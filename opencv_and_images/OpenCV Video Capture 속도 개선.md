# OpenCV Video Capture

Video capture 관련 속도 저하 문제가 발생하였다. 해상도가 너무 높아서 발생하는 문제인지 확인하였으나, 해상도 문제는 아니었다.



독특하게도 실행 시간이 오래될수록, 즉 로드된 프레임이 많을수록 속도의 저하 현상이 발견되었다. 함수별 소요 시간은 cProfile 라이브러리를 이용해 확인하였다.



1. 10 프레임만 봤을 때

| ncalls | tottime | percall | cumtime | percall | filename:lineno(function)                     |
| ------ | ------- | ------- | ------- | ------- | --------------------------------------------- |
| 11     | 2.943   | 0.268   | 2.943   | 0.268   | {method 'set' of 'cv2.VideoCapture' objects}  |
| 232    | 0.86    | 0.004   | 0.86    | 0.004   | {waitKey}                                     |
| 11     | 0.494   | 0.045   | 0.494   | 0.045   | {method 'read' of 'cv2.VideoCapture' objects} |



2. 60 프레임 봤을 때

| ncalls | tottime | percall | cumtime | percall | filename:lineno(function)                     |
| ------ | ------- | ------- | ------- | ------- | --------------------------------------------- |
| 60     | 53.214  | 0.887   | 53.214  | 0.887   | {method 'set' of 'cv2.VideoCapture' objects}  |
| 580    | 2.751   | 0.005   | 2.751   | 0.005   | {waitKey}                                     |
| 60     | 2.691   | 0.045   | 2.691   | 0.045   | {method 'read' of 'cv2.VideoCapture' objects} |



cv2.VideoCapture.set 과 cv2.VideoCapture.read 에서 속도 저하가 심하다는 것을 확인할 수 있었다. 



기존 코드였던 `self.vidcap.set(cv2.CAP_PROP_POS_FRAMES, frameNumber)` 을 `self.vidcap.set(cv2.CAP_PROP_FPS, frameNumber)`으로 변경하였다. 아래 방식은 메모리에 미리 영상을 로드하는 방식이고 위의 방식은 disk에서 직접 가져오는 방식이라고 한다. 약 4~6배 정도 속도가 개선되었다. 



## Reference

https://stackoverrun.com/ko/q/12457368