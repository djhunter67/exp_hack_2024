from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from pydantic import BaseModel
from models import JSONModel

app = FastAPI(
    title="eXp 2024 Hacking",
    description="This is an API endpoint for AI + Twilio",
    version="0.1.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

data = JSONModel("database.json")

class Message(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # Get all the messages from the database
    messages = data.read_all()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request, "messages": messages},
    )


@app.post("/twilio/whatsapp")
async def read_results(message: Message):
    data.create({"message": message.message})
    return {"message": message.message}


@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/imgs/ca_icon.ico")
