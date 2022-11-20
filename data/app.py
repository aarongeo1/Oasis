from fastapi import FastAPI

app = FastAPI()



@app.get("/hack/{lat}/{long}")
async def read_item(lat,long):
    return {"lat": lat,"long":long}
