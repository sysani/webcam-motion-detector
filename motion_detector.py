import cv2

video = cv2.VideoCapture(0)

while True:
    check, frame = video.read()
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Capturing",grey)
    key = cv2.waitKey(2000)
    if key == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
