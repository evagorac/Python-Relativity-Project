import math
import random

def dist(a,b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2)**.5

iterations = 1000000
sum = 0.

for x in range(iterations):
    point1 = (math.cos(random.random() * 2 * math.pi),math.sin(random.random() * 2 * math.pi))
    point2 = (math.cos(random.random() * 2 * math.pi),math.sin(random.random() * 2 * math.pi))
    sum += dist(point1,point2)

print(sum / iterations)
