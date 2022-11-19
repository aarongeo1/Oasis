import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from itertools import product

def makeFDPlot(sourceFile, city, longkey, latkey):
    dataFrame = pd.read_csv(sourceFile)
    longitude = dataFrame[longkey].values
    latitude = dataFrame[latkey].values

    longrange = [min(longitude), max(longitude)]
    latrange = [min(latitude), max(latitude)]

    longval = np.linspace(*longrange, 500)
    latval = np.linspace(*latrange, 500)

    longmesh, latmesh = np.meshgrid(longval, latval, indexing='ij')

    distMesh = np.zeros(np.shape(longmesh))

    for i,j in product(range(len(longval)),range(len(latval))):
        loDist = longitude-longmesh[i][j]
        laDist = latitude - latmesh[i][j]
        dist = np.sqrt(loDist**2 + laDist**2)
        distMesh[i][j] = np.min(dist)
    plt.imshow(distMesh,
               interpolation='spline36',
               origin='lower',
               cmap=plt.cm.get_cmap('viridis_r'),
               extent=longrange+latrange)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(f'Distance From Nearest Grocery Store - {city}')
    cbar = plt.colorbar()
    cbar.ax.set_ylabel('Coordinate Distance')
    plt.savefig(f'plots/{city}Plot.jpg')

makeFDPlot('cleandata/calgary.csv', 'Calgary', 'longitude', 'latitude')
makeFDPlot('cleandata/edmonton.csv', 'Edmonton', 'Longitude', 'Latitude')
