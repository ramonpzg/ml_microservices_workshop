from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Mount the 'templates' folder to serve HTML files
templates = Jinja2Templates(directory="./templates")


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/service1")
async def read_page1(request: Request):
    return templates.TemplateResponse("page1.html", {"request": request})

@app.get("/service2")
async def read_page2(request: Request):
    return templates.TemplateResponse("page2.html", {"request": request})