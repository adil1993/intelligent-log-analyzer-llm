from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from .routes import router

app = FastAPI(title="Intelligent Log Analyzer")

templates = Jinja2Templates(directory="app/templates")

app.include_router(router)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})