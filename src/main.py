from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from pydantic import BaseModel
from .models import JSONModel
import uuid
from typing import Dict, Any, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="eXp 2024 Hacking",
    description="This is an API endpoint for AI + Twilio",
    version="0.1.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

data = JSONModel("database.json")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],   # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],   # Allows all headers
)

class Message(BaseModel):
    account_sid: str
    api_version: str
    body: str
    date_created: str
    date_sent: str
    date_updated: str
    direction: str
    error_code: str
    error_message: str
    from_: str
    num_media: str
    num_segments: str
    price: str
    price_unit: str
    messaging_service_sid: str
    sid: str
    status: str
    subresource_uris: Dict[str, str]
    tags: Dict[str, str]
    to: str
    uri: str

app = FastAPI()

class SubresourceUris(BaseModel):
    media: str

class Tags(BaseModel):
    campaign_name: str
    message_type: str

class FormData(BaseModel):
    account_sid: str
    api_version: str
    body: str
    date_created: str
    date_sent: str
    date_updated: str
    direction: str
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    from_: str = Form(..., alias="from")
    num_media: str
    num_segments: str
    price: Optional[str] = None
    price_unit: Optional[str] = None
    messaging_service_sid: str
    sid: str
    status: str
    subresource_uris: SubresourceUris
    tags: Tags
    to: str
    uri: str


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
async def read_results(message: FormData):
    id = str(uuid.uuid4())
    account_sid: str = Form(...),
    api_version: str = Form(...),
    body: str = Form(...),
    date_created: str = Form(...),
    date_sent: str = Form(...),
    date_updated: str = Form(...),
    direction: str = Form(...),
    error_code: Optional[str] = Form(None),
    error_message: Optional[str] = Form(None),
    from_: str = Form(..., alias="from"),
    num_media: str = Form(...),
    num_segments: str = Form(...),
    price: Optional[str] = Form(None),
    price_unit: Optional[str] = Form(None),
    messaging_service_sid: str = Form(...),
    sid: str = Form(...),
    status: str = Form(...),
    subresource_uris: Dict[str, str] = Form(...),
    tags: Dict[str, str] = Form(...),
    to: str = Form(...),
    uri: str = Form(...),


    data.create({
        "id": id,
        "account_sid": account_sid,
        "api_version": api_version,
        "body": body,
        "date_created": date_created,
        "date_sent": date_sent,
        "date_updated": date_updated,
        "direction": direction,
        "error_code": error_code,
        "error_message": error_message,
        "from": from_,
        "num_media": num_media,
        "num_segments": num_segments,
        "price": price,
        "price_unit": price_unit,
        "messaging_service_sid": messaging_service_sid,
        "sid": sid,
        "status": status,
        "subresource_uris": subresource_uris,
        "tags": tags,
        "to": to,
        "uri": uri,
    })
    return {
        "success": True,
        "id": id
    }


@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/imgs/ca_icon.ico")


