# Python openCV

## Video read

예제 코드

```	python
import cv2
import matplotlib.pyplot as plt

cap = cv2.VideoCapture("myVideo.mp4")
frame_number = 100

cap.set(cv2.CAP_PROP_POS_FRAMEs, frame_number)
ret, frame1 = cap.read()

frame1 = cv2.cvtColor(frame1, cv2.BGR2GRAY)
plt.imshow(frame1, cmap='gray')
plt.show()
```



가장 먼저 원하는 비디오 파일을 VideoCapture 함수의 인자로 전달한다. 



cap.set에 Frame을 따로 지정하지 않으면 가장 첫 프레임부터 불러오지만 원하는 프레임을 지정할 수 있다.



여기에서는 그냥 plt 를 이용해서 이미지를 플랏하였다. 참고로  openCV는 BGR을 사용하기 때문에 plt.imshow 함수를 이용해 이미지를 불러오려면 img = cv2.cvtColor(img, BGR2RGB) 를 이용해서 변환시켜주어야 한다.