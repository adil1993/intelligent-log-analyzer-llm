
from fastapi import APIRouter, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .services.analyzer import analyze_logs

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.post("/analyze", response_class=HTMLResponse)
async def analyze(
    request: Request,
    log_text: str = Form(None),
    log_file: UploadFile = File(None)
):
    content = None

    if log_file and log_file.filename:
        file_bytes = await log_file.read()
        if file_bytes:
            content = file_bytes.decode()

    if not content and log_text:
        content = log_text.strip()

    if not content:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": "No logs provided.", "log_text": log_text}
        )

    result = await analyze_logs(content)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": result, "log_text": log_text}
    )
