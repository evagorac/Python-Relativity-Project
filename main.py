import cv2
import numpy as np
import sys

window = (512,512)
vert_dist = 3000000. #meters
mpp = vert_dist/window[1] * .9 #metersperpixel * percent dist of height
origin = (window[0]/2,window[1])

#define shape in pixels in normal coordinate space
shape = np.array([[0,0],[32,64]], np.int32)
shape *= mpp

#finds lowest point to define what distance refers to
lowestH = shape[0]
for x in shape:
    if x[1] < lowestH[1]:
        lowestH = x

#define constants
pos = (0,0) #inital starting position
rapidity = .8

#equation derived
def mapPoint(coord):
    return (-coord[0] * rapidity**2 - rapidity*(coord[0]**2 + coord[1]**2 - rapidity**2 * coord[1]**2)**.5)/(rapidity**2 - 1)

#used to change from normal frame to inverted y frame
def transformCoordinate((x,y)):
    return (x,-y)

#SEGMENTED POINTS MADE HERE
segmented_values = []
for vertex in range(len(shape)-1):
    v1 = shape[vertex]
    v2 = shape[vertex+1]
    m = (v2[1]-v1[1])/(v2[0]-v1[0])
    b = v1[1] - (m * v[0])
    segmented_x_values = np.linspace(v1[0],v2[0],num = ( (v2[0]-v1[0])**2 + (v2[1]-v1[1])**2 )**.5)
    for x in segmented_x_values:
        segmented_values.append((x,m*x+b))

#main loop
#DEFINED IN NORMAL COORDINATE SPACE
for pixelDisplacement in range(pos,2 * (origin[0] - pos)):
    dx = pixelDisplacement * mpp
    

    #MUST BE TRANSFORMED TO TOP LEFT ORIGIN FRAME
    #IMAGE IS PRINTED
    img = np.ones((window[0],window[1])) * 255
    for x in range(len(transformed)-1):
        copy = img
        v1 = x[0]
        v2 = x[1]
        cv2.line(copy, (0,0), (x,x), (0,0,0), 4)
        cv2.imshow('test',copy)
        key = cv2.waitKey(2)
        if (key == ord("q")):
            cv2.destroyAllWindows()
            sys.exit()








#use linspace
