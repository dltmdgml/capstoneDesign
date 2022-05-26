# Using CCTV image sample data, make abnormal behavior detection model
# CCTV 이미지 샘플데이터를 이용한 이상행동 탐지 모델 제작
### 개요
먼저 프로젝트 주제선정 배경 및 개요입니다. 나라지표의 사이트 정보에 따르면 국내 공공기관 CCTV 설치 및 증가대수는 해가 갈수록 점점 증가하는 추세이며, 범죄가 발생하면 CCTV를 확보하는 것이 우선이 될 정도로 강력사건의 결정적인 역할을 하면서 해결사로 떠오르고 있습니다. 한편으로는 CCTV가 사후 범인 검거 능력은 탁월하지만 범죄 예방 효과는 크지 않다는 우려가 있습니다. 또한 범죄 예방을 위해 지속적으로 입력되는 영상을 사람이 직접 감시하고 비정상 행위를 검출하는 일은 한계가 있습니다. 따라서 범죄 예방 및 운영 효율성을 증대시키기 위해서는 자동으로 비정상적인 이벤트를 검출하고 추적하기 위한 영상 분석 기술이 필요하다고 생각하여 프로젝트 주제를 이와 같이 정하였습니다.

### 프로젝트 내용
- 데이터 준비
  - 데이터 다운로드 <br>
    [지하철 역사 내 CCTV 이상행동 영상 이미지](https://aihub.or.kr/aidata/34122) <br>
    13개의 이상행동 데이터 + 7개의 객체 데이터
  - dataset.yaml 생성
    ```
    path: /content/drive/MyDrive/custom_dataset  # root 디렉토리
    train: /content/drive/MyDrive/custom_dataset/train.txt  # 학습데이터 경로
    val: /content/drive/MyDrive/custom_dataset/val.txt

    # Classes
    nc: 20  #  class 개수
    names: [ "turnstile_trespassing", "turnstile_wrong_direction", "stairway_fall", "property_damage", "spy_camera", "wandering", "fainting", "escalator_fall", "unattended", "theft", "public_intoxication", "assault", "surrounding_fall", "wheelchair", "blind", "stroller", "drunk", "merchant", "child", "person"]  # class 이름들
    ```
   - 디렉토리 구조
    ```bash
      └── custom_dataset
          ├── train
          │   ├── Part1
          │   │   ├── images
          │   │   └── labels
          │   │   ...      
          │   └── Part6
          └── validation
          │   ├── Part1
          │   │   ├── images
          │   │   └── labels
          │   └── Part2
          ├── train.txt
          └── validation.txt
- 데이터 전처리
  - 라벨 생성
    ![label_made](imgs_for_readmefile/annotation.PNG)
- 모델 학습
  [yolov5m](https://github.com/ultralytics/yolov5) 사용 <br>
  image size: 640(권장) <br>
  batch size: 32(컴퓨터 메모리가 수행할 수 있는 가장 큰 batch size 권장) <br>
  epoch number: 300(권장) <br>
- 모델 테스트
- 모델의 결과 시각화
  웹 페이지 구현과 웹 서버를 구축하며 결과를 한눈에 알아보기 쉽도록 하였습니다.
### 일정
![일정](imgs_for_readmefile/schedule.PNG)
### 요구사항
![요구사항명세서_1](imgs_for_readmefile/requirments_analysis.PNG)
### 아키텍처
![architecture](imgs_for_readmefile/architecture1.PNG)
### 설계
#### UI 설계서
![UI설계서_2](imgs_for_readmefile/UI_2.PNG)
![UI설계서_3](imgs_for_readmefile/UI_3.PNG)
![UI설계서_4](imgs_for_readmefile/UI_4.PNG)
### 테스트
![테스트](imgs_for_readmefile/test.PNG)
### FILE STRUCTURE
| File/Directory | Decscription |
| ------ | ------ |
| [src](src) | 프로젝트 전체 소스 |
| [imgs_for_test](imgs_for_test) |test를 위한 이미지와 동영상 |
| [포스터]([22년 1학기 캡스톤-포스터-LK(이승희)].pptx) | 포스터 PPT |
| [포스터]([22년 1학기 캡스톤-포스터-LK(이승희)].pdf) | 포스터 PDF |
| [발표자료](발표.pptx) | 발표자료 PPT |
| [시연영상](시연영상-LK팀.mp4) | 시연영상 |
| [결과보고서](2022년_1학기_캡스톤디자인_결과보고서.hwp) | 결과보고서 |

**소스 코드 테스트 시 [src] 폴더 아래에서 실행**<br>
**flask와 yolov5 종속성 설치 필요**
anaconda prompt 실행 <br>
'''
pip install flask
cd [your_path]/src/
pip install -r yolov5/requirements.txt
'''
vscode에서 실행 <br>
마켓플레이스에서 flask-snippets, python 설치 <br>
ctrl + shiht + p > python:select interpreter > flask가 설치되어 있는 환경 선택<br>
[your_path]/src/ 폴더 열기 > app.py 실행 <br>
터미널에 출력되는 주소로 접속하여 테스트
