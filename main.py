import cv2
import numpy as np
import sys

c = 3000 #km/s
rapidity = .8
window = (750,750)

#relative to observer
xRange = (-3*c,3*c)
yRange = (0*c,4*c)

#define kilometers per pixel in each direction
xKmpp = (xRange[1] - xRange[0])/window[0]
yKmpp = (yRange[1] - yRange[0])/window[1]

hOffset = -(xRange[0]+xRange[1])/2/xKmpp
vOffset = (yRange[0]+yRange[1])/2/yKmpp

#always center relative to coordinate axis
observer = np.array([[int(window[0]/2 + hOffset) * xKmpp,int(window[1]/2 + vOffset) * yKmpp]])

#define shape in kilometers in space
shape1 = np.array([
[0.,-1*c],
[-0.2245*c,-0.309*c],
[-0.9511*c,-0.309*c],
[-0.3633*c,0.118*c],
[-0.5878*c,0.809*c],
[0,0.382*c],
[0.5878*c,0.809*c],
[0.3633*c,0.118*c],
[0.9511*c,-0.309*c],
[0.2245*c,-0.309*c],
[0.,-1*c],
])

shape2 = np.array([
[0,0],
[c,0],
[c,-2*c],
[-c,-2*c],
[-c,0],
[0,0],
[0,.5*c],
[-2*c,.5*c],
[-2*c,1.5*c],
[-2*c,.5*c],
[2*c,.5*c],
[2*c,-.5*c],
[2*c,.5*c],
[0,.5*c],
[0,3*c],
[1.7321*c,2*c],
[2.7321*c,3.7321*c],
[1.7321*c,2*c],
[-1.7321*c,4*c],
[-2.7321*c,2.2679*c]
])

shape = shape2

#contraction
gamma = 1/(1-rapidity**2)**.5
shape[:,0] /= gamma

#inital starting position in kilometers relative to observer
startingPos = np.array([-5*c,-5*c])

#defines shape relative to observer
shape[:] += startingPos[:]

#takes shape relative to observer and fits it into the window
def transformShape(x):
    a = np.copy(x)
    #print(shape)
    a[:,0] /= (2 * xKmpp)
    a[:,1] /= (2 * yKmpp)
    a[:,0] += observer[0][0]/xKmpp
    a[:,1] += observer[0][1]/yKmpp
    #print(shape)
    #print("\n\n\n")
    return a

#equation derived
def findOffset(coord):
    return (-coord[0] * rapidity**2 + rapidity*(coord[0]**2 + coord[1]**2 - rapidity**2 * coord[1]**2)**.5)/(rapidity**2 - 1)

#SEGMENTED POINTS MADE HERE
#transforms shape into itself with more verticies to show curves perceived
segmented_values = []
for vertex in range(len(shape)-1):
    v1 = shape[vertex]
    v2 = shape[vertex+1]
    if(v1[0]!=v2[0]):
        m = (v2[1]-v1[1])/(v2[0]-v1[0])
        b = v1[1] - (m * v1[0])
        segmented_x_values = np.linspace(v1[0],v2[0],num = 20)
        for x in segmented_x_values:
            segmented_values.append((x,m*x+b))
    else:
        y_space = np.linspace(v1[1],v2[1],num = 20)
        for a in y_space:
            segmented_values.append((v1[0],a))

img = np.ones((window[0],window[1])) * 255
cv2.rectangle(img,(int(observer[0][0]/xKmpp-8),int(observer[0][1]/yKmpp-8)),(int(observer[0][0]/xKmpp+8),int(observer[0][1]/yKmpp+8)),(0,0,0),2)

#main loop
#TODO fix the main loop like in class
#for dx in range(int(startingPos[0] + observer[0][0]),3 * int(-startingPos[0] + observer[0][0]),int(-2 * startingPos[0] / 250)):
for dx in range(0,int(window[0]*xKmpp) - startingPos[0],int(window[0]*xKmpp/500)):
    perceivedCoords = []
    for x in segmented_values:
        #map point and transform into image display frame
        q = findOffset((x[0]+dx,x[1]))
        #print(dx)
        #print("MAPPED OFFSET WRT OBSERVER: \n" + str(q))
        perceivedCoords.append((x[0]+q+dx,x[1]))

    transformedCoords = transformShape(np.array(perceivedCoords))
    # print("POINT ON WINDOW: \n " + str(transformedCoords) + "\n\n")

    copy = np.copy(img)
    actualCoords = []
    for x in shape:
        actualCoords.append((x[0]+dx,x[1]))
    actualCoords = transformShape(actualCoords)
    for x in range(len(actualCoords)-1):
        v1 = actualCoords[x]
        v2 = actualCoords[x+1]
        cv2.line(copy, (int(v2[0]) , int(v2[1])) , (int(v1[0]) , int(v1[1])) , (0,0,0) , 2)

    for x in range(len(transformedCoords)-1):
        v1 = transformedCoords[x]
        v2 = transformedCoords[x+1]
        # print((int(v2[0]) , int(v2[1])))
        # print((int(v1[0]) , int(v1[1])))
        # print("\n")
        cv2.line(copy, (int(v2[0]) , int(v2[1])) , (int(v1[0]) , int(v1[1])) , (0,255,255) , 2)
    cv2.imshow('I should be doing my college apps right now',copy)
    # unContracted = np.ones((window[0],window[1])) * 255
    # still = shape2
    # still[:] += startingPos[:]
    # still = transformShape(still)
    # for x in range(len(still)-1):
    #     v1 = still[x]
    #     v2 = still[x+1]
    #     cv2.line(unContracted, (int(v2[0]) , int(v2[1])) , (int(v1[0]) , int(v1[1])) , (0,255,255) , 2)
    #cv2.imshow("un-contracted image", unContracted)
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
