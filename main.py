import cv2
import numpy as np
import sys
img = np.ones((512,512)) * 255
for x in range(512):
    copy = img
    cv2.line(copy, (0,0), (x,x), (0,0,0), 4)
    cv2.imshow('test',copy)
    key = cv2.waitKey(2)
    if (key == ord("q")):
        cv2.destroyAllWindows()
        sys.exit()
window = (512,512)
vert_dist = 3000000. #meters
mpp = vert_dist/window[1] * .9 #metersperpixel * percent dist of height
origin = (window[0]/2,window[1])

#define shape
shape = np.array([[0,0],[32,64]], np.int32)

maxH = shape[0]
for x in shape:
    if x[1] > maxH[1]:
        maxH = x


#define constants
pos = (0,0) #inital starting position
rapidity = .8

#equation derived
def transformPoint(coord):
    return (-coord[0] * rapidity**2 - rapidity*(coord[0]**2 + coord[1]**2 - rapidity**2 * coord[1]**2)**.5)/(rapidity**2 - 1)

#main loop
for pixelDist in range(pos,2 * (origin[0] - pos)):





#use linspace
