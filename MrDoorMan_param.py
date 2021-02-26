import numpy as np
import cv2 as cv
import time
import picamera
import picamera.array

from gpiozero import Button, LED

reset_button = Button(17)
capture_button = Button(22)
running_LED = LED(4)
running_LED.off()
signal = LED(27)
signal.off()

state = False
bgimage = []

with picamera.PiCamera() as camera:
    camera.start_preview()
    time.sleep(2)
    with picamera.array.PiRGBArray(camera) as stream:
        while True:
            camera.capture(stream, format='bgr')
            if (reset_button == True):
                time.sleep(1)
                for i in range(3):
                    running_LED.on()
                    time.sleep(0.5)
                    running_LED.off()
                    time.sleep(0.5)
                bgimage = cv.cvtColor(stream.array, cv.COLOR_BGR2GRAY)
                cv.imshow('bg', bgimage)
                cv.waitKey(0)
            else:
                if (len(bgimage) ~= 0 ):
                    if (capture_button == True):
                        image = cv.cvtColor(stream.array, cv.COLOR_BGR2GRAY)
                        diff_img = cv.subtract(image, bgimage)
                        diff_value = np.sum(diff_img > 100)
                        print(diff_value)
                        cv.imshow('img', image)
                        cv.imshow('diffimg', diff_img)
                        cv.imshow('thrimg', diff_img > 100)
                        cv.waitKey(0)
                        

