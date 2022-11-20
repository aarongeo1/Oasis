import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from itertools import product
from boundary import edmontonBoundary, calgaryBoundary
from haversine import haversine

def extractLongLat(srcFile, longkey, latkey):
    dataFrame = pd.read_csv(srcFile)
    longitude = dataFrame[longkey].values
    latitude = dataFrame[latkey].values
    return longitude, latitude

def computeDistances(long, lat, longList, latList):
    dist = [haversine(long,
                      lat,
                      storeLong,
                      storeLat)
            for storeLong, storeLat in zip(longList, latList)]
    return dist

def makeFDPlot(sourceFile, city, longkey, latkey, boundary):
    longitude, latitude = extractLongLat(sourceFile, longkey, latkey)
    longbound, latbound = boundary

    extendRatio = 0.1
    longrange = [min(longbound), max(longbound)]
    longdiff = longrange[1]-longrange[0]
    longrange[0] -= extendRatio*longdiff
    longrange[1] += extendRatio*longdiff

    latrange = [min(latbound), max(latbound)]
    latdiff = latrange[1] - latrange[0]
    latrange[0] -= extendRatio*latdiff
    latrange[1] += extendRatio*latdiff
    longval = np.linspace(*longrange, 500)
    latval = np.linspace(*latrange, 500)

    longmesh, latmesh = np.meshgrid(longval, latval, indexing='ij')

    distMesh = np.zeros(np.shape(longmesh))

    for i,j in product(range(len(longval)),range(len(latval))):
        dist = computeDistances(longmesh[i][j],
                                latmesh[i][j],
                                longitude,
                                latitude)
        distMesh[i][j] = np.min(dist)
    plt.imshow(distMesh,
               #interpolation='spline36',
               origin='lower',
               cmap=plt.cm.get_cmap('viridis_r'),
               extent=longrange+latrange)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(f'Distance From Nearest Grocery Store - {city}')
    cbar = plt.colorbar()
    cbar.ax.set_ylabel('Distance (km)')
    plt.plot(longbound, latbound, color='black')
    plt.savefig(f'plots/{city}Plot.jpg')
    plt.clf()

makeFDPlot('cleandata/calgary.csv', 'Calgary', 'longitude', 'latitude', calgaryBoundary)
makeFDPlot('cleandata/edmonton.csv', 'Edmonton', 'Longitude', 'Latitude', edmontonBoundary)
