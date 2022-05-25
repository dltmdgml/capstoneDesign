import os
import glob
import time
import cv2
import torch
from flask import Flask, render_template, flash, request, Response
from werkzeug.utils import secure_filename 
import subprocess
import requests
import json

UPLOAD_VIDEO_FOLDER = './uploads/videos/'
UPLOAD_IMAGE_FOLDER = './uploads/images/'
DETECT_FOLDER = './yolov5/runs/detect/'

img_ext = ['.jpg', '.png', '.jpeg', '.JPG', '.PNG','.JPEG']    # 허용되는 이미지 확장자
video_ext = ['.mp4', '.avi', '.mov', '.wmv']  # 허용되는 비디오 확장자

def send_the_message(class_name):
    msg_content = '다음과 같은 이상행동이 발생했습니다. [' + str(class_name) + ']'
    with open("kakao_code.json","r") as fp:
        tokens = json.load(fp)

    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    headers={
        "Authorization" : "Bearer " + tokens["access_token"]
    }
    data={
        "template_object": json.dumps({
            "object_type": "text",
            "text": msg_content,
            "link":{
                "web_url":"#"  #link 필수 사항
            }
        })
    }
    response = requests.post(url, headers=headers, data=data)
    response.status_code
    
    #메시지 전송 여부 확인
    if response.json().get('result_code') == 0:
        print('메시지를 성공적으로 보냈습니다.')
    else:
        print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))  # 오류 발생시 토큰 다시 발급받아야 함
        print(msg_content)

# model result(xy point, predict score, class) parse
def score_frame(frame, model):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model.to(device)
    results = model(frame)
    print(f"results: {results}")
    labels = results.xyxyn[0][:, -1].numpy()
    cord = results.xyxyn[0][:, :-1].numpy()
    return labels, cord

# 바운딩 박스 그리기
def plot_boxes(results, frame):
    labels, cord = results
    n = len(labels)
    x_shape, y_shape = frame.shape[1], frame.shape[0]
    for i in range(n):
        row = cord[i]
        # If score is less than 0.2 we avoid making a prediction.
        if row[4] < 0.2: 
            continue
        x1 = int(row[0]*x_shape)
        y1 = int(row[1]*y_shape)
        x2 = int(row[2]*x_shape)
        y2 = int(row[3]*y_shape)
        box_h = y2 - y1
        bgr = (0, 255, 0) # color of the box
        classes = model.names # Get the name of label index
        label_font = cv2.FONT_HERSHEY_SIMPLEX #Font for the label.
        text = classes[int(labels[i])]
        size, BaseLine = cv2.getTextSize(text,label_font,box_h*0.003,1)
        cv2.rectangle(frame, \
                      (x1, y1), (x2, y2), \
                       bgr, 2) #Plot the boxes
        cv2.putText(frame,\
                    text,\
                    (x1, y1+size[1]), \
                    label_font, box_h*0.003, bgr, 2) #Put a label over box.

        # send message
        class_name = str(classes[int(labels[i])])
        if class_name in classes_cnts: 
            classes_cnts[class_name] += 1
            if classes_cnts[class_name] >= 10:
                classes_cnts[class_name] = 0  # count 초기화
                send_the_message(class_name)

    return frame  # 인식된 객체 바운딩 박스 그린 후 frame 리턴

# Flask 객체를 app에 할당
app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_VIDEO_FOLDER'] = UPLOAD_VIDEO_FOLDER
app.config['UPLOAD_IMAGE_FOLDER'] = UPLOAD_IMAGE_FOLDER
app.config["SECRET_KEY"] = "ABCD"  # for flash message


# 업로드 HTML 렌더링
@app.route('/')
def index():
    [os.remove(f) for f in glob.glob('./uploads/images/*')]
    [os.remove(f) for f in glob.glob('./uploads/videos/*')]
    [os.remove(f) for f in glob.glob('./static/exp/*')]
    [os.remove(f) for f in glob.glob('./extracted_images/*')]
    return render_template('main.html')

# 실시간 영상 스트리밍
@app.route('/Streaming', methods=['GET','POST'])
def Streaming():
    return render_template('subPage1.html')

#실시간 영상 스트리밍
@app.route('/video_feed')
def video_feed():
    def generate(): # 데이터를 생성하는 생성기
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # webcam
        while 1:
            ret, img = cap.read()
            # img = cv2.flip(img, 1) #좌우 반전
            results = score_frame(img, model)
            frame = plot_boxes(results, img)
            if frame is None:       
                frame = cv2.imencode('.jpg', img)[1].tobytes()   # 객체가 추출되지 않아도 이미지 show
            else:
                frame = cv2.imencode('.jpg', frame)[1].tobytes()
            # yield 브라우저에 직접 전송됨
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.01)
    # 응답 객체에 generate()함수 넘김
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


#파일 업로드 처리
@app.route('/FileUpload', methods=['GET','POST'])
def FileUpload():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        ext_text = os.path.splitext(filename)[1]
        # VIDEO
        if ext_text in video_ext:
            start = time.time()
            file.save(os.path.join(app.config['UPLOAD_VIDEO_FOLDER'], filename))
            print('video upload success')
            subprocess.run(['python', './yolov5/detect.py', '--weights', 'model_anomaly/best.pt', '--img', '640', '--source', app.config['UPLOAD_VIDEO_FOLDER'], '--data', 'model_anomaly/custom_dataset_1.yaml'])
            print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
        # IMAGE
        elif ext_text in img_ext:
            start = time.time()
            file.save(os.path.join(app.config['UPLOAD_IMAGE_FOLDER'], filename))
            print('image upload success')
            img = cv2.imread(os.path.join(app.config['UPLOAD_IMAGE_FOLDER'], filename))   
            # img = cv2.resize(img, (0,0), fx=0.7, fy=0.7)
            results = score_frame(img, model)
            frame = plot_boxes(results, img)
            cv2.imwrite(os.path.join('static/exp/', filename), frame)
            print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
        else:
            ext_text = ""
            flash("지원하지 않는 파일 형식입니다. 파일의 확장자를 확인해 주세요.")
        return render_template('subPage2.html', file_name=filename, ext_text=ext_text)
    else:
        return render_template('subPage2.html')

if __name__ == '__main__':
    #count 초기화
    cnt0=0 
    cnt1=0 
    cnt2=0 
    cnt3=0 
    cnt4=0 
    cnt5=0 
    cnt6=0 
    cnt7=0 
    cnt8=0 
    cnt9=0 
    cnt10=0 
    cnt11=0 
    cnt12=0
    cnt13=0
    cnt14=0
    
    classes_cnts = { "turnstile_trespassing": cnt0, "turnstile_wrong_direction": cnt1, "stairway_fall": cnt2, \
                        "property_damage": cnt3, "spy_camera" : cnt4, "wandering" : cnt5, "fainting" : cnt6, \
                        "escalator_fall" : cnt7, "unattended" : cnt8, "theft" : cnt9, "public_intoxication" : cnt10, \
                        "assault" : cnt11, "surrounding_fall" : cnt12, "person" : cnt13, "cup" : cnt14 }
    
    # 모델 로드
    # model = torch.hub.load('ultralytics/yolov5', 'custom', path='model_anomaly/best.pt')
    model = torch.hub.load('ultralytics/yolov5', 'yolov5m')

    app.run(host="0.0.0.0", port=80, debug=True)
