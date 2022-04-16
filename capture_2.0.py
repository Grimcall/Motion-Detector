import cv2
import numpy as np

first_frame = None
video = cv2.VideoCapture(1)
video.set(cv2.CAP_PROP_POS_FRAMES, 20)

while True:

    #Cap
    check, frame = video.read()  
    
    #Calculate Difference
    prepared_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    
    prepared_frame = cv2.GaussianBlur(src=prepared_frame, ksize=(5, 5), sigmaX=0)
    
    #Set previous frame and continue if there is none.
    if first_frame is None:
        first_frame = prepared_frame
        continue 

    #Calculate difference and update previous frame
    diff_frame = cv2.absdiff(first_frame, prepared_frame)
    first_frame = prepared_frame

    #Dilute image to make differences more visible.
    kernel = np.ones((5,5))
    diff_frame = cv2.dilate(diff_frame, kernel, 1)

    #Create threshold B&W frame.
    thresh_delta = cv2.threshold(src = diff_frame, thresh=20, maxval=255, type=cv2.THRESH_BINARY)[1]
    
    #thresh_delta = cv2.dilate(thresh_delta, None, iterations = 0)

    (cnts,_ ) = cv2.findContours(image=thresh_delta, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 1000:
            continue

        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 3) 

    cv2.imshow("Prepared Frame", prepared_frame)
    cv2.imshow("Delta Frame", diff_frame)
    cv2.imshow("Threshhold Frame", thresh_delta)
    cv2.imshow("Main", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
 


video.release()
cv2.destroyAllWindows()