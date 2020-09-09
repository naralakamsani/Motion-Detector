# Make imports
import cv2
from datetime import datetime
import pandas

#Define first frame before recording
first_frame = None

#store data of recording to video
video = cv2.VideoCapture(0)

status_list = [None, None]
times = []

while True:
    check, frame = video.read()

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame
        continue
        
    #Find the difference between current frame and first frame
    delta_frame = cv2.absdiff(first_frame, gray_frame)

    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=1)

    #Find the contours or objects not in the first frame
    (cnts, _) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    status = 0
    for countour in cnts:
        if cv2.contourArea(countour) < 1000:
            continue
        status = 1

        (x, y, w, h) = cv2.boundingRect(countour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)

    status_list.append(status)
    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())

    cv2.imshow("gray", gray_frame)
    cv2.imshow("delta", delta_frame)
    cv2.imshow("thresh", thresh_frame)
    cv2.imshow("frame", frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        if status_list == 1:
            times.append(datetime.now)
        break
#print the times
print(times)

df = pandas.DataFrame(columns=["Start", "End"])
for i in range(0, len(times), 2):
    df = df.append({"Start": times[i], "End": times[i + 1]}, ignore_index=True)

    df.to_csv("Time of motion.csv")

video.release()
cv2.destroyAllWindows()
