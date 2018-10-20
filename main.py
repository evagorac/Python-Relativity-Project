import cv2
import numpy as np
import sys

c = 3000 #km/s
rapidity = .8
window = (512,512)

#relative to observer
xRange = (-10*c,10*c)
yRange = (-5*c,5*c)

#define kilometers per pixel in each direction
xKmpp = (xRange[1] - xRange[0])/window[0]
yKmpp = (yRange[1] - yRange[0])/window[1]

#always center relative to coordinate axis
observer = np.array([[int(window[0]/2) * xKmpp,int(window[1]/2) * yKmpp]])

#define shape in kilometers in space
shape = np.array([[0.,0.],[.1*c,-3*c]])

#inital starting position in kilometers relative to observer
startingPos = np.array([-4*c,-1*c])

#defines shape relative to observer
shape[:] += startingPos[:]

#takes shape relative to observer and fits it into the window
def transformShape(x):
    a = np.copy(x)
    #print(shape)
    a[:,0] /= (2 * xKmpp)
    a[:,1] /= (2 * yKmpp)
    a[:,0] += window[0]/2
    a[:,1] += window[1]/2
    #print(shape)
    #print("\n\n\n")
    return a

#equation derived
def mapPoint(coord):
    return ((-coord[0] * rapidity**2 + rapidity*(coord[0]**2 + coord[1]**2 - rapidity**2 * coord[1]**2)**.5)/(rapidity**2 - 1), coord[1])

#SEGMENTED POINTS MADE HERE
#transforms shape into itself with more verticies to show curves perceived
segmented_values = []
for vertex in range(len(shape)-1):
    v1 = shape[vertex]
    v2 = shape[vertex+1]
    m = (v2[1]-v1[1])/(v2[0]-v1[0])
    b = v1[1] - (m * v1[0])
    segmented_x_values = np.linspace(v1[0],v2[0],num = 10)
    for x in segmented_x_values:
        segmented_values.append((x,m*x+b))
        #print([x,m*x+b])

img = np.ones((window[0],window[1])) * 255
cv2.rectangle(img,(int(window[0]/2-4),int(window[1]/2-4)),(int(window[0]/2+4),int(window[1]/2+4)),(0,0,0),2)

#main loop
#TODO fix the main loop like in class
for dx in range(int(startingPos[0] + observer[0][0]),int(-startingPos[0] + observer[0][0]),int(-2 * startingPos[0] / 250)):
    #print("pos[0]: {}\npos[1]: {}\ndx: {}".format(pos[0],pos[1],dx))
    perceivedCoords = []
    for x in segmented_values:
        #map point and transform into image display frame
        q = mapPoint((x[0]+dx,x[1]))
        print(dx)
        print("MAPPED POINT WRT OBSERVER: \n" + str(q))
        perceivedCoords.append(mapPoint(q))

    transformedCoords = transformShape(np.array(perceivedCoords))
    # print("POINT ON WINDOW: \n " + str(transformedCoords) + "\n\n")

    copy = np.copy(img)
    for x in range(len(transformedCoords)-1):
        v1 = transformedCoords[x]
        v2 = transformedCoords[x+1]
        # print((int(v2[0]) , int(v2[1])))
        # print((int(v1[0]) , int(v1[1])))
        # print("\n")
        #cv2.line(copy, (int(v2[0]) , int(v2[1])) , (int(v1[0]) , int(v1[1])) , (0,0,0) , 2)
        cv2.line(copy, (int(v2[0]) , int(v2[1])) , (int(v1[0]) , int(v1[1])) , (0,0,0) , 2)
    cv2.imshow('test',copy)
    key = cv2.waitKey(2)
    if (key == ord("q")):
        cv2.destroyAllWindows()
        sys.exit()
# copy = np.copy(img)
# for x in range(len(segmented_values)-1):
#     v1 = segmented_values[x]
#     v2 = segmented_values[x+1]
#     print("shape after :" + str([v1[0],v1[1],v2[0],v2[1]]))
#     cv2.line(copy, (int(v2[1]/mpp),int(v1[1]/mpp)), (int(v2[0]/mpp),int(v1[0]/mpp)), (0,0,0), 1)
#     cv2.imshow('test',copy)
#     key = cv2.waitKey(2)
#     if (key == ord("q")):
#         cv2.destroyAllWindows()
#         sys.exit()


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
