# -*- coding: utf-8 -*-
import cv2
import numpy
import serial as ser

class HumanDetector():
    """HumanDetector class. User .detectFaces to get rectangles containing faces"""
    def __init__(self, cascadePath):
        self.cascade = cv2.CascadeClassifier(cascadePath)

    def detectHumans(self, img):
        grayFrame   = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces       = self.cascade.detectMultiScale(grayFrame, 1.5, 5)
        for (x, y, w, h) in faces:
            img         = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_color   = img[y:y+h, x:x+w]

        return faces


class CamController():

    modes = { ### HAELP!!!
        "auto": "a",
        "90Degrees": "t",
        "manual": "m"
    }

    def __init__(self, port, baudrate):
        self.console = ser.Serial(port, baudrate)
        self.mode = "auto"
        self.console.write(modes[self.mode]) ### See comment on line 27

    def __changeMode__(self, mode):
        self.mode = mode ### Mathias? you know your codes
        # self.console.write(modes[self.mode])

    def distanceFromCenter(self, face, img):
        rows,cols,_     = img.shape
        center          = (cols/2, rows/2)
        deltaX          = face[0] + face[2]/2
        deltaY          = face[1] + face[3]/2
        return (center[0]-deltaX, center[1]-deltaY)

    def moveXY(self, img, face):
        rows,cols,_ = img.shape
        center      = (cols/2, rows/2)
        delta = self.distanceFromCenter(face, img)
        if abs(delta[0]) > 5:
            # write to console to move x (delta[0]/abs(delta[0])) ### sending only ±1º at a time bc idc about perfect resolution
            dist = (delta[0]/abs(delta[0]))
            # print(dist)
            self.console.write("X" + str(dist))
        if abs(delta[1]) > 5:
            # write to console to move y (delta[1]/abs(delta[1]))
            dist = (delta[1]/abs(delta[1]))
            # print(dist)
            self.console.write("Y" + str(dist))

def main():
    detector        = HumanDetector('haarcascade_frontalface_default.xml')
    camController   = CamController("/dev/tty/wtf", 11500)

    try:

        while True:
            videoFeed   = cv2.VideoCapture(0)

            _, img      = videoFeed.read()
            img         = cv2.resize(img, (640, 360))
            faces       = detector.detectHumans(img)

            if camController.mode == "auto":
                try:
                    camController.moveXY(img, faces[0])
                except Exception as e:
                    print(e)
                    pass
            elif camController.mode == "manual":
                pass
            elif camController.mode == "90Degrees":
                self.console.write(str(cv2.waitKey() & 0xFF))

            cv2.imshow('Faces', img)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break
        videoFeed.release()
        cv2.destroyAllWindows()

    except KeyboardInterrupt:
        print("All done")

main()
