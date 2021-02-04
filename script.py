
import cv2

face_cascade = cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")
img = cv2.imread("./imgs/photo.jpg")
grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

face_coords = face_cascade.detectMultiScale(grey_img, scaleFactor=1.2, minNeighbors=5)
#returns x & y coords of first point, and the width and height

for (x, y, w, h) in face_coords:
    img = cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 3)

cv2.imshow("grey",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
