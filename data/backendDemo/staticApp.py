from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from math import radians, cos, sin, asin, sqrt
import csv
import numpy as np
import matplotlib.pyplot as plt
import random

app = FastAPI()
templates = Jinja2Templates(directory="jinjaTemplates")

app.mount("/plots", StaticFiles(directory="../plots"), name="plots")
app.mount("/staticRes", StaticFiles(directory="staticRes"), name="staticRes")



@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html.jinja", {"request": request})

@app.get("/test", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("hack.html", {"request": request})

@app.get("/calgary", response_class=HTMLResponse)
async def calgary_page(request: Request):
    return templates.TemplateResponse("calgary.html.jinja", {"request": request})

@app.get("/edmonton", response_class=HTMLResponse)
async def edmonton_page(request: Request):
    return templates.TemplateResponse("edmonton.html.jinja", {"request": request})

@app.get("/hack/{lat}/{long}", response_class=HTMLResponse)
async def read_item(request: Request, lat,long):
    latVal = float(lat)
    longVal = float(long)
    distVal = getDist(float(lat),float(long))
    city = determineCity(float(lat),float(long))
    if city == "Edmonton":
        imgLink = genSmallPlot(longVal, latVal, "../cleandata/Edmonton.npz")
    else:
        imgLink = genSmallPlot(longVal, latVal, "../cleandata/Calgary.npz")

    return templates.TemplateResponse("sample.html", {"request": request,
                                                              "lat": latVal,
                                                              "long": longVal,
                                                              "nearDist": distVal,
                                                              "imgLink": imgLink})

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

    rval = random.randint(0,10000)
    fname = f"../plots/plot{rval}.jpg"
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(f'Distance From Nearest Grocery Store')
    cbar = plt.colorbar()
    cbar.ax.set_ylabel('Distance (km)')
    plt.savefig(fname)
    plt.clf()
    return f"/plots/plot{rval}.jpg"

def getDist(lat2,long2):
    kmmin = 99999999999999999
    latmin = 0
    longmin = 0
    with open("../cleandata/calgary.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            lat1 = float(row.get("latitude"))
            long1 = float(row.get("longitude"))
            km = haversine(long1, lat1, long2, lat2)
            if kmmin > km:
                kmmin = km
                latmin = lat1
                longmin = long1

    with open("../cleandata/edmonton.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            lat1 = float(row.get("Latitude"))
            long1 = float(row.get("Longitude"))
            km = haversine(long1, lat1, long2, lat2)
            if kmmin > km:
                kmmin = km
                latmin = lat1
                longmin = long1
    return(kmmin)

def determineCity(longVal, latVal):
    calData = np.load("../cleandata/Calgary.npz")
    calLat = calData['latitude']
    calLong = calData['longitude']

    edmData = np.load("../cleandata/Edmonton.npz")
    edmLat = edmData['latitude']
    edmLong = edmData['longitude']


    withinCalLong = min(calLong) <= longVal <= max(calLong)
    withinCalLat = min(calLat) <= latVal <= max(calLat)
    withinEdmLong = min(edmLong) <= longVal <= max(edmLong)
    withinEdmLat = min(edmLat) <= longVal <= max(edmLat)

    print(withinCalLong)
    print(withinCalLat)
    print(withinEdmLong)
    print(withinEdmLat)
    if withinCalLong or withinCalLat:
        return "Calgary"
    elif withinEdmLong or withinEdmLat:
        return "Edmonton"
    else:
        return None

def haversine(lon1, lat1, lon2, lat2):

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6371* c
    return km