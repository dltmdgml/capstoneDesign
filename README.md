# Using CCTV image sample data, make abnormal behavior detection model
## CCTV 이미지 샘플데이터를 이용한 이상행동 탐지 모델 제작
### 개요
먼저 프로젝트 주제선정 배경 및 개요입니다. 나라지표의 사이트 정보에 따르면 국내 공공기관 CCTV 설치 및 증가대수는 해가 갈수록 점점 증가하는 추세이며, 범죄가 발생하면 CCTV를 확보하는 것이 우선이 될 정도로 강력사건의 결정적인 역할을 하면서 해결사로 떠오르고 있습니다. 한편으로는 CCTV가 사후 범인 검거 능력은 탁월하지만 범죄 예방 효과는 크지 않다는 우려가 있습니다. 또한 범죄 예방을 위해 지속적으로 입력되는 영상을 사람이 직접 감시하고 비정상 행위를 검출하는 일은 한계가 있습니다. 따라서 범죄 예방 및 운영 효율성을 증대시키기 위해서는 자동으로 비정상적인 이벤트를 검출하고 추적하기 위한 영상 분석 기술이 필요하다고 생각하여 프로젝트 주제를 이와 같이 정하였습니다.
### 일정

### 요구사항
![요구사항명세서_1](imgs_for_readmefile/requirments_analysis.PNG)
### 아키텍처
![architecture](imgs_for_readmefile/architecture.PNG)
### 설계
#### UI 설계서
![UI설계서_2](imgs_for_readmefile/UI_2.PNG)
![UI설계서_3](imgs_for_readmefile/UI_3.PNG)
![UI설계서_4](imgs_for_readmefile/UI_4.PNG)
### 프로젝트 내용
- 데이터 준비
  - 데이터 다운로드 
    [지하철 역사 내 CCTV 이상행동 영상 이미지](https://aihub.or.kr/aidata/34122)
    13개의 이상행동 데이터 + 7개의 객체 데이터
  - dataset.yaml 생성
    ```
    path: /content/drive/MyDrive/custom_dataset  #root 디렉토리
    train: /content/drive/MyDrive/custom_dataset/train.txt  # 학습데이터 경로
    val: /content/drive/MyDrive/custom_dataset/val.txt

    # Classes
    nc: 20  #  class 개수
    names: [ "turnstile_trespassing", "turnstile_wrong_direction", "stairway_fall", "property_damage", "spy_camera", "wandering", "fainting", "escalator_fall", "unattended", "theft", "public_intoxication", "assault", "surrounding_fall", "wheelchair", "blind", "stroller", "drunk", "merchant", "child", "person"]  # class 이름들
    ```
- 데이터 전처리
  - 라벨 생성
    ![label_made](imgs_for_readmefile/annotation.PNG)
- 모델 학습
  image size: 640(권장)
  batch size: 32(컴퓨터 메모리가 수행할 수 있는 가장 큰 batch size 권장)
  epoch number: 300(권장)
  ```
  !python train.py --img 640 --batch 32 --epoch 300 --data [dataset.yaml path] --weight [weight path(.pt)]
  ```
- 모델 테스트
- 웹 페이지 & 서버 개발
### 테스트
