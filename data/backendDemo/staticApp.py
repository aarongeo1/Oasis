from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="jinjaTemplates")

app.mount("/plots", StaticFiles(directory="../plots"), name="plots")
app.mount("/staticRes", StaticFiles(directory="staticRes"), name="staticRes")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html.jinja", {"request": request})

@app.get("/calgary", response_class=HTMLResponse)
async def calgary_page(request: Request):
    return templates.TemplateResponse("calgary.html.jinja", {"request": request})

@app.get("/edmonton", response_class=HTMLResponse)
async def edmonton_page(request: Request):
    return templates.TemplateResponse("edmonton.html.jinja", {"request": request})