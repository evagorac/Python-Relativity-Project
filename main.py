import cv2
import numpy as np
import sys

c = 3000 #km/s
rapidity = .8
window = (960,960)

#relative to observer
xRange = (-10*c,10*c)
yRange = (-5*c,15*c)

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

shape = np.copy(shape2)

#contraction
gamma = 1/(1-rapidity**2)**.5
shape[:,0] /= gamma

#inital starting position in kilometers relative to observer
#I just found out that a horizontal offset fucks the whole thing up
startingPos = np.array([0,-5*c])

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
cv2.rectangle(img,(int(observer[0][0]/xKmpp-8),int(observer[0][1]/yKmpp-16)),(int(observer[0][0]/xKmpp+8),int(observer[0][1]/yKmpp)),(0,0,0),2)
copy = np.copy(img)
#main loop
#TODO fix the main loop like in class
for dx in range(2 * xRange[0],int(window[0]*xKmpp + xRange[1]),int(window[0]*xKmpp/500)):
#for dx in [-12000,0,12000]:
    print(dx)
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
        cv2.line(copy, (int(v2[0]) , int(v2[1])) , (int(v1[0]) , int(v1[1])) , (0,0,0) , 4)

    for x in range(len(transformedCoords)-1):
        v1 = transformedCoords[x]
        v2 = transformedCoords[x+1]
        # print((int(v2[0]) , int(v2[1])))
        # print((int(v1[0]) , int(v1[1])))
        # print("\n")
        cv2.line(copy, (int(v2[0]) , int(v2[1])) , (int(v1[0]) , int(v1[1])) , (0,120,0) , 4)
    # if dx == -12000:
    #     cv2.imwrite("1.jpg",copy)
    # elif dx == 0:
    #     cv2.imwrite("2.jpg",copy)
    # elif dx == 12000:
    #     cv2.imwrite("3.jpg",copy)
    #cv2.imwrite("all.jpg",copy)
    # unContracted = np.ones((window[0],window[1])) * 255
    # still = shape2
    # still = transformShape(still)
    # for x in range(len(still)-1):
    #     v1 = still[x]
    #     v2 = still[x+1]
    #     cv2.line(unContracted, (int(v2[0]) , int(v2[1])) , (int(v1[0]) , int(v1[1])) , (0,0,0) , 2)
    # cv2.imwrite("un-contracted_image.jpg", unContracted)\
    cv2.imshow('I should be doing my college apps right now',copy)
    key = cv2.waitKey(2)
    if (key == ord("q")):
        cv2.destroyAllWindows()
        sys.exit()


print("ok")
