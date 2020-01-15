import cv2 as cv
import numpy as np


cv.namedWindow('EGASma') # create the window
vc = cv.VideoCapture(0) # open default webcam

numb = 0
face_cascade = cv.CascadeClassifier('haarcascades/haarcascade_frontalface_alt.xml')

if vc.isOpened(): # webcam successfully recognized
    retval = True
    while retval:
        retval, frame = vc.read()
        cv.line(img=frame, pt1=(10, 10), pt2=(100, 10), color=(255, 255, 255), thickness=5, lineType=8, shift=0)
        face_detect = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)
        for (x, y, w, h) in face_detect:
            cv.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 6)
            if (numb % 6 == 0):
                print(numb)
                cv.imwrite('Frames/Disguist_{:0>6}.jpg'.format(numb), frame[y:y+h, x:x+w])
        cv.imshow('EGASma', frame)
        numb += 1
        key = cv.waitKey(1) # wait for press any key for certain miliseconds
        if key == 27: # exit on ESC
            break
cv.destroyWindow('EGASma')