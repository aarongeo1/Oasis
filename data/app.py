from fastapi import FastAPI
import csv
from haversine import haversine

app = FastAPI()


@app.get("/hack/{lat}/{long}")
async def read_item(lat,long):
    return {"lat": lat,"long":long}

def get(lat2,long2):
    kmmin = 99999999999999999
    latmin = 0
    longmin = 0
    with open(r"C:\Users\Aaron Geo Binoy\Desktop\hack\idk-yet\data\cleandata\calgary.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            lat1 = float(row.get("latitude"))
            long1 = float(row.get("longitude"))
            km = haversine(long1, lat1, long2, lat2)
            if kmmin > km:
                kmmin = km
                latmin = lat1
                longmin = long1

    with open(r"C:\Users\Aaron Geo Binoy\Desktop\hack\idk-yet\data\cleandata\edmonton.csv") as f:
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

if __name__ == "__main__":
    lat2 = 53.51214
    long2 = -113.5322387
    dict = read_item(lat2,long2)
    lat2 = dict.get("lat")
    long2 = dict.get("long")
    km = get(lat2,long2)
