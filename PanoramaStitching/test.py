import cv2

# 마우스 이벤트 콜백함수 정의
def mouse_callback(event, x, y, flags, param):
    global coordinates
    if event == cv2.EVENT_LBUTTONDOWN:
        # print("마우스 이벤트 발생, x:", x ," y:", y) # 이벤트 발생한 마우스 위치 출력
        print("event")
        coordinates.append([x, y])

coordinates = []

img = cv2.imread('yosemite1.jpg')

cv2.namedWindow('image')  #마우스 이벤트 영역 윈도우 생성
cv2.setMouseCallback('image', mouse_callback)
print(coordinates)

while(True):

    cv2.imshow('image', img)

    k = cv2.waitKey(1) & 0xFF
    if k == ord('s'):    # ESC 키 눌러졌을 경우 종료
        print("ESC 키 눌러짐")
        break
    elif len(coordinates) >= 4:
        print(coordinates)
        break

cv2.destroyAllWindows()