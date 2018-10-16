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
vert_dist = 3000000 #meters
mpp = vert_dist/window[1] #metersperpixel
origin = (256,512)



#use linspace
