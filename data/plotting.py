import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from itertools import product
from boundary import edmontonBoundary, calgaryBoundary
from haversine import haversine
import random

def genSmallPlot(longVal, latVal, cityFile):

    cityData = np.load(cityFile)
    cityLong = cityData['longitude']
    cityLat = cityData['latitude']
    distData = cityData['distMesh']
    indLat = np.searchsorted(cityLat, latVal)
    indLong = np.searchsorted(cityLong, longVal)


    sliceLat = slice(max(0,indLat - 25), indLat + 25)
    sliceLong = slice(max(0,indLong - 25), indLong + 25)

    plt.imshow(distData[sliceLat, sliceLong],
               #interpolation='spline36',
               origin='lower',
               cmap=plt.cm.get_cmap('viridis_r'),
               extent=(
                   min(cityLong[sliceLong]),
                   max(cityLong[sliceLong]),
                   cityLat[sliceLat][0],
                   max(cityLat[sliceLat])
               ))

    fname = f"plots/plot{random.randint(0,10000)}.jpg"
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(f'Distance From Nearest Grocery Store')
    cbar = plt.colorbar()
    cbar.ax.set_ylabel('Distance (km)')
    plt.savefig(fname)
    plt.clf()
    return fname




def determineCity(longVal, latVal):
    calData = np.load("/cleandata/Calgary.npz")
    calLat = calData['latitude']
    calLong = calData['longitude']

    edmData = np.load("/cleandata/Edmonton.npz")
    edmLat = edmData['latitude']
    edmLong = edmData['longitude']

    withinCalLong = min(calLong) <= longVal <= max(calLong)
    withinCalLat = min(calLat) <= latVal <= max(calLat)
    withinEdmLong = min(edmLong) <= longVal <= max(edmLong)
    withinEdmLat = min(edmLat) <= longVal <= max(edmLat)
    if withinCalLong and withinCalLat:
        return "Calgary"
    elif withinEdmLong and withinEdmLat:
        return "Edmonton"
    else:
        return None

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

    np.savez(f'cleandata/{city}.npz',
             distMesh = distMesh,
             longMesh = longmesh,
             latMesh = latmesh,
             longitude = longitude,
             latitude = latitude)
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

#makeFDPlot('cleandata/calgary.csv', 'Calgary', 'longitude', 'latitude', calgaryBoundary)
#makeFDPlot('cleandata/edmonton.csv', 'Edmonton', 'Longitude', 'Latitude', edmontonBoundary)

testLat = 53.4336516
testLong = -113.6226629
print(genSmallPlot(testLong, testLat, 'cleandata/Edmonton.npz'))