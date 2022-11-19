import pandas as pd
import numpy as np

def cityBoundary(srcFile,key):
    bFrame = pd.read_csv(srcFile)
    polygonString = bFrame[key].values[0]
    polygonString = polygonString.lstrip('MULTIPOLYGON (((')
    polygonString = polygonString.rstrip(')))')
    coordPairs = polygonString.split(', ')
    coordPairs = [pair.split(' ') for pair in coordPairs]
    longVal = np.array([float(pair[0]) for pair in coordPairs])
    latVal = np.array([float(pair[1]) for pair in coordPairs])
    return longVal, latVal

def withinPolygon(x,y,polyX, polyY):

    n = len(polyX)
    inside = False

    p1x = polyX[0]
    p1y = polyY[0]
    for i in range(n+1):
        p2x = polyX[i % n]
        p2y = polyY[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y
    return inside


calgaryBoundary = cityBoundary('rawdata/calgaryBoundary.csv','MULTIPOLYGON')
edmontonBoundary = cityBoundary('rawdata/edmontonBoundary.csv', 'the_geom')