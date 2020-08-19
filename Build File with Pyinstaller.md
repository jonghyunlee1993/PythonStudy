# Pyinstall를 이용한 배포 파일 만들기

- 배포 파일은 사용자의 OS에 따라 결정된다.
  - 맥이나 리눅스라면 wine 을 이용해서 exe를 만들 수 있다.
- 배포 파일은 가상 환경에 설치되어 있는 라이브러리에 영향을 받는 듯하다.
  - Conda, venv 등으로 적합한 환경을 구성하고 배포 파일을 만들자.
- pyinstaller를 이용하면 엄청 간단하게 배포 파일을 만들 수 있다.
  - `pip install pyinstaller`
  - `pyinstaller -F --onefile runme.py`
- Dist 라는 폴더 아래에 exe 파일이 생성된다. 이걸 배포하면 된다. 
  - 만약 해당 exe가 요구하는 텍스트 파일 등이 있다면 상대 경로로 설정해주어야 하며, 해당 상대 경로에 넣어주면 된다. 