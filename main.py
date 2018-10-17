import cv2
import numpy as np
import sys

c = 3000000.
window = (512,512)
vert_dist = 1 * c #meters
mpp = vert_dist/window[1] * .9 #metersperpixel * percent dist of height
origin = (window[0]/2.,window[1])

#define shape in pixels in normal coordinate space
shape = np.array([[0,0],[.1*c,.1*c]], np.int32)
shape = shape * mpp

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
    return ((-coord[0] * rapidity**2 - rapidity*(coord[0]**2 + coord[1]**2 - rapidity**2 * coord[1]**2)**.5)/(rapidity**2 - 1), coord[1])

#used to change from normal frame to inverted y frame
def transformCoordinate(x):
    return (x[0],-x[1])

#SEGMENTED POINTS MADE HERE
segmented_values = []
for vertex in range(len(shape)-1):
    v1 = shape[vertex]
    v2 = shape[vertex+1]
    m = (v2[1]-v1[1])/(v2[0]-v1[0])
    b = v1[1] - (m * v1[0])
    segmented_x_values = np.linspace(v1[0],v2[0],num = ( (v2[0]-v1[0])**2 + (v2[1]-v1[1])**2 )**.5)
    for x in segmented_x_values:
        segmented_values.append((x,m*x+b))

#main loop
#DEFINED IN NORMAL COORDINATE SPACE
for pixelDisplacement in range(pos[0],int(2 * (origin[0] - pos[0])),5):
    dx = (pixelDisplacement * mpp)/2
    transformed = []
    for x in segmented_values:
        #map point and transform into image display frame
        transformed.append(transformCoordinate(mapPoint((x[0]+dx,x[1]))))

    img = np.ones((window[0],window[1])) * 255
    cv2.polyline(img,transformed,True,(0,255,255),1)
    cv2.imshow('test',copy)
    key = cv2.waitKey(2)
    if (key == ord("q")):
        cv2.destroyAllWindows()
        sys.exit()

"""
    for x in range(len(transformed)-1):
        copy = img
        v1 = transformed[x]
        v2 = transformed[x+1]
        cv2.line(copy, (int(v2[1]),int(v1[1])), (int(v2[0]),int(v1[0])), (0,0,0), 4)
        cv2.imshow('test',copy)
        key = cv2.waitKey(2)
        if (key == ord("q")):
            cv2.destroyAllWindows()
            sys.exit()
"""







#use linspace
