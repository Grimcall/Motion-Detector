import cv2, time, pandas
import numpy as np
from datetime import datetime

#InitFrames and Capture + Motion List decl + Time list decl.
first_frame = None
motion_events = [None, None]
times = []
df = pandas.DataFrame(columns=["Start", "End"])

#Set VideoCapture to an address ranging from 0 to n, a video file (.mp4, avi...) or other video source. Mine is set to my webcam.
video = cv2.VideoCapture(1)
video.set(cv2.CAP_PROP_POS_FRAMES, 20)

while True:

    #Framerate Adjust
    time.sleep(0.1)
    #Capture Declaration
    check, frame = video.read()
    motion_status = 0  
    
    #Grayscale and blur
    prepared_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    
    prepared_frame = cv2.GaussianBlur(src=prepared_frame, ksize=(5, 5), sigmaX=0)
    
    #Set previous frame and continue if there is none.
    if first_frame is None:
        first_frame = prepared_frame
        continue 

    #Calculate difference and update previous frame
    diff_frame = cv2.absdiff(first_frame, prepared_frame)
    first_frame = prepared_frame

    #Dilate image to make differences more visible.
    kernel = np.ones((5,5))
    diff_frame = cv2.dilate(diff_frame, kernel, 1)

    #Create threshold B&W frame.
    thresh_delta = cv2.threshold(src = diff_frame, thresh=20, maxval=255, type=cv2.THRESH_BINARY)[1]
    
    #Draw rectangles
    (cnts,_ ) = cv2.findContours(image=thresh_delta, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)

    #The larger the number, the larger the object contour.
    obj_size = 5000
    for contour in cnts:
        if cv2.contourArea(contour) < obj_size:
            continue
        motion_status = 1
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 3) 
    motion_events.append(motion_status)

    motion_status = motion_events[-2:]
    
    if motion_events[-1] == 1 and motion_events[-2] == 0:
        times.append(datetime.now())
    if motion_events[-1] == 0 and motion_events[-2] == 1:
        times.append(datetime.now())

    #Uncomment to see how the motion capture process works
    #cv2.imshow("Prepared Frame", prepared_frame)
    #cv2.imshow("Delta Frame", diff_frame)
    #cv2.imshow("Threshhold Frame", thresh_delta)
    cv2.imshow("Main", frame)

    #Press Q to exit.
    key = cv2.waitKey(1)
    if key == ord('q'):
        if motion_status == 1:
            times.append(datetime.now())
        break
    
#FURTHER TESTING REQUIRED    
for i in range(0, (len(times))-1, 2):
    df = df.append({"Start": times[i], "End": times[i+1]}, ignore_index = True)

df.to_csv("Motion_Events.csv")

video.release()
cv2.destroyAllWindows()