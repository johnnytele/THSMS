import cv2 
import numpy as np

capture = cv2.VideoCapture(0)

# History Threshold DetectShadows
fgbg = cv2.createBackgroundSubtractorMOG2(300, 400, True)

frameCount = 0
while(1):
    ret, frame = capture.read()

    #checks if the current frame actually exists
    if not ret:
        break

    frameCount += 1

    frameCount += 1

    print('Frame: %d, Pixel Count: %d' % (frameCount, count))

    if (frameCount > 1 and count > 5000):
        print('snn')

    cv2.imshow('frame', resizedFrame)
    cv2.imshow('Mask', fgmask)




capture.release()
cv2.destroyAllWindows()