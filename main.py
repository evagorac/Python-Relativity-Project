import cv2
import numpy as np
import sys

c = 3000 #km/s
window = (512,512)
vert_dist = 1 * c #kilometers
scale = 1
mpp = vert_dist/window[1] * scale #kilometersperpixel to make every window scaled uniformly * scale
observer = (int(window[0]/2),0) #observer position always top middle

#define shape in kilometers in space
shape = np.array([[0,0],[.1*c,.2*c]], np.int32)
shape = shape / mpp
#shape is now defined in pixels

#finds lowest point to define what distance refers to
lowestH = shape[0]
for x in shape:
    if x[1] < lowestH[1]:
        lowestH = x

#define constants
pos = (-c,c) #inital starting position in kilometers relative to observer
rapidity = .8

#equation derived
def mapPoint(coord):
    return ((-coord[0] * rapidity**2 - rapidity*(coord[0]**2 + coord[1]**2 - rapidity**2 * coord[1]**2)**.5)/(rapidity**2 - 1), coord[1])

#used to change from normal frame to inverted y frame\
#not used
def transformCoordinate(x):
    return (x[0],-x[1])

#transforms relative pos to absolute pos relative to coordinate space
#TODO check this to make sure its correct
def findAbsolutePos(x):
    return (x[0] - observer[0] * mpp, x[1])

#SEGMENTED POINTS MADE HERE
#transforms shape into intself with more verticies to show curves perceived
segmented_values = []
for vertex in range(len(shape)-1):
    v1 = shape[vertex]
    v2 = shape[vertex+1]
    m = (v2[1]-v1[1])/(v2[0]-v1[0])
    b = v1[1] - (m * v1[0])
    segmented_x_values = np.linspace(v1[0],v2[0],num = 10)
    for x in segmented_x_values:
        segmented_values.append((x,m*x+b))
        print([x,m*x+b])

img = np.ones((window[0],window[1])) * 255
#TODO show where observer is

#reassign pos in terms of absolute coordinates
pos = findAbsolutePos(pos)

#main loop
#TODO fix the main loop like in class
for pixelDisplacement in range(int(pos[0]/mpp),int((2 * (observer[0] - pos[0]))/mpp),5):
    dx = (pixelDisplacement * mpp)/2
    transformed = []
    for x in segmented_values:
        #map point and transform into image display frame
        transformed.append(transformCoordinate(mapPoint((x[0]+dx,x[1]-lowestH[1]))))
    copy = img
    for x in range(len(transformed)-1):
        v1 = transformed[x]
        v2 = transformed[x+1]
        print("shape after :" + str([v1[0],v1[1],v2[0],v2[1]]))
        cv2.line(copy, (int(v2[1]/mpp),int(v1[1]/mpp)), (int(v2[0]/mpp),int(v1[0]/mpp)), (0,0,0), 1)
        cv2.imshow('test',copy)
        key = cv2.waitKey(2)
        if (key == ord("q")):
            cv2.destroyAllWindows()
            sys.exit()


print("ok")

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
"""
    cv2.polylines(img,transformed,True,(0,255,255),1)
    cv2.imshow('test',copy)
    key = cv2.waitKey(2)
    if (key == ord("q")):
        cv2.destroyAllWindows()
        sys.exit()
"""
