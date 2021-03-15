import cv2, pandas
from datetime import datetime
from face_detection import detect_face

first_frame = None
video = cv2.VideoCapture(0)
status_list = [None]
times = []
motion_df = pandas.DataFrame(columns=["Start", "End"])
count = 0
face_status = False

while True:
    check, frame = video.read()
    status = 0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21),0)

    if first_frame is None:
        first_frame = gray
        continue

    delta_frame = cv2.absdiff(first_frame, gray)
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    (cntrs,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cntrs:
        if cv2.contourArea(contour) < 1000:
            continue

        status = 1

        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,255), 3)

    #store time of motion entering & exiting frame
    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())

    #check if face is detected in motion & save to imgs folder
    if detect_face(frame):
        if face_status == False:
            count+=1
            cv2.imwrite(filename='./imgs/saved_img'+str(count)+'.jpg', img=frame)
            face_status = True
    else:
        face_status = False


    cv2.imshow("Capturing", gray)
    cv2.imshow("Delta", delta_frame)
    cv2.imshow("Threshold", thresh_frame)
    cv2.imshow("Colour Frame", frame)

    key = cv2.waitKey(100)
    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break

    print(status_list)

for i in range(0,len(times),2):
    motion_df = motion_df.append({"Start": times[i], "End":times[i+1]}, ignore_index=True)

motion_df.to_csv("times.csv")
video.release()
cv2.destroyAllWindows()
