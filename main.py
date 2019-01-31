import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

filename = 'video.mp4'
fps = 10.0
res = '720p'

def changeRes(img, w, h):
    img.set(3, w)
    img.set(4, h)

dimension = {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160)
}

def getDimensions(img, res="1080p"):
    w, h = dimension["480p"]
    if res in dimension:
        w, h = dimension[res]
    changeRes(img, w, h)
    return w, h

img = cv2.VideoCapture(0)
dims = getDimensions(img, res=res)

while(True):
    ret, frame = img.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.5, 5)
    for (x,y,w,h) in faces:
        frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
    	    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)


    cv2.imshow('Faces', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# cv2.imshow('img',img)
# cv2.waitKey(0)

img.release()
cv2.destroyAllWindows()
