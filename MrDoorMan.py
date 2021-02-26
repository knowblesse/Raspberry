import numpy as np
import cv2 as cv
import time
import picamera
import picamera.array

from gpiozero import Button, LED

reset_button = Button(17)
running_LED = LED(4)
running_LED.off()
signal = LED(5)
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
            else:
                if (len(bgimage) ~= 0 ):
                    image = cv.cvtColor(stream.array, cv.COLOR_BGR2GRAY)
                    diff_img = cv.subtract(image, bgimage)
                    diff_value = np.sum(diff_img > 100)
                    time.sleep(0.5)
                    print(diff_value)

