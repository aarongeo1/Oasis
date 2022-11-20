from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/plots", StaticFiles(directory="../plots"), name="plots")