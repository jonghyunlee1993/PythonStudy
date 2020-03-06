# Vatic 사용법

vatic은 video annotation tool 

공식 링크

https://github.com/cvondrick/vatic



docker 파일도 있는데 아래의 링크에서 설치 방법을 안내해준다. (도커가 훨씬 쉽다)

https://github.com/NPSVisionLab/vatic-docker



작업 예시

![image-20200305174150558](/home/jonghyun/.config/Typora/typora-user-images/image-20200305174150558.png)



데이터 베이스 초기화

```bash
turkic setup --database --reset
```



프레임 추출(영상을 프레임 단위 이미지 모음으로 분해)

```bash
turkic extract /path/to/video.mp4 /path/to/output/directory
  --no-resize
```



영상을 import, 사용할 레이블을 입력해준다

```bash
turkic load identifier /path/to/output/directory Label1 Label2 LabelN
```



로컬 작업용 publish

```bash
turkic publish --offline
```



작업 링크는 아래에서 id만 계속 바꿔준다.

http://localhost:8111/?id=1&hitId=offline



몇 개의 작업이 생성되었는지 확인

```bash
turkic status
```



작업 결과 저장

```bash
turkic dump identifier -o output.txt
```