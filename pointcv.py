import math
import random
import numpy as np
import cv2

# Image size
x = 600
y = 600
# Iterations of Flips
n = 40000

# Initial configutations

# 3 pt configurations
# pts = [(random.randint(0, 5), random.randint(0,5)) for i in range(3)] 

# 4 pt configurations
pts = [(random.randint(0, 5), random.randint(0,5)) for i in range(4)] 

def scalepoly(pts, x, y):
    ''' scale and shift poly to fit img '''
    midx, midy = x/2, y/2
    maxx, maxy = map(lambda l: max(l), zip(*pts))
    scalex, scaley = .5*(x/(2*maxx)), .5*(y/(2*maxy))
    #scale
    scaled = [(scalex*x, scaley*y) for (x,y) in pts]
    #shift
    shifted = [(x+midx, y+midy) for (x,y) in scaled]
    return shifted

def drawpts(pts):
    ''' Draw list of points on image '''
    [cv2.circle(img, (int(x), int(y)), 1, (255,255,255), -1) for (x,y) in  pts]
    return

def midpoint(seg):
    ''' Return midpt of start-end segment 
    Segment given as tuple ((x0,y0), (x1,y1)) '''
    return map(lambda x : .5*(x[0]+x[1]), zip(*seg))

def perpbisector(seg):
    ''' return perp bisector of a seg = (start, end)
     Returns (m,b) where perp bisector is y = mx + b '''
    (mpx, mpy) = midpoint(seg)
    (x0, y0) = seg[0]
    (x1, y1) = seg[1]
    try:
        m = -(x1-x0)/(y1-y0)
    except ZeroDivisionError:
        # x = mpx is the bisector
        return (None, mpx)
    b = -m*mpx + mpy
    return (m, b)
    
def reflect(pt, seg):
    ''' Reflect a pt over a perpbisector of seg '''
    (m,b) = perpbisector(seg)
    if not m:
        return (2*b - pt[0], pt[1])
    (x0, y0) = pt
    d = (x0 + m*(y0-b))/(1+m**2)
    return (2*d - x0, 2*m*d + 2*b- y0)

def flip(pts, j):
    ''' Perform flip on vertex j, return new pts '''
    start = (j-1) % len(pts)
    end = (j+1) % len(pts)
    seg = (pts[start], pts[end])
    pts[j] = reflect(pts[j], seg)
    return pts

def plotflips(pts, n):
    ''' Perform n random flips on pts, plot pts '''
    temp = scalepoly(pts, 600, 600)
    for i in range(n):
        j = random.randint(0, len(pts)-1)
        temp = flip(temp, j)
        drawpts(temp)
    return

if __name__ == '__main__':
    # Setup image
    img = np.zeros((x,y,3), np.uint8)

    # Flip and display
    plotflips(pts, n)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
