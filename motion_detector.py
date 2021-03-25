import cv2, pandas
from datetime import datetime
from face_detection import detect_face

first_frame = None
status_list = [None]
face_status = False
motion_times = []
face_times = []
motion_df = pandas.DataFrame(columns=["Start", "End"])
face_df = pandas.DataFrame(columns=["Start", "End"])
count = 0

video = cv2.VideoCapture(0)

while True:
    check, frame = video.read()
    motion_status = 0
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
        if cv2.contourArea(contour) < 10000:
            continue

        motion_status = 1

        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,255), 3)

    #store time of motion entering & exiting frame
    status_list.append(motion_status)
    status_list = status_list[-2:]

    if status_list[-1]==1 and status_list[-2]==0:
        motion_times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        motion_times.append(datetime.now())

    #check if face is detected in motion
    if detect_face(frame):
        if face_status == False:
            count+=1
            face_times.append(datetime.now())
            cv2.imwrite(filename='./imgs/saved_img'+str(count)+'.jpg', img=frame)
            face_status = True
    else:
        if face_status == True:
            face_times.append(datetime.now())
        face_status = False

    cv2.imshow("Colour Frame", frame)

    key = cv2.waitKey(100)
    if key == ord('q'):
        if motion_status == 1:
            motion_times.append(datetime.now())
        if face_status == True:
            face_times.append(datetime.now())
        break

for i in range(0,len(motion_times),2):
    motion_df = motion_df.append({"Start": motion_times[i], "End":motion_times[i+1]}, ignore_index=True)

for i in range(0, len(face_times), 2):
    face_df = face_df.append({"Start": face_times[i], "End":face_times[i+1]}, ignore_index=True)

motion_df.to_csv("times.csv")
face_df.to_csv("face.csv")
video.release()
cv2.destroyAllWindows()
