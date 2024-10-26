from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from pydantic import BaseModel
from .models import JSONModel
import uuid
from typing import Dict, Any

app = FastAPI(
    title="eXp 2024 Hacking",
    description="This is an API endpoint for AI + Twilio",
    version="0.1.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

data = JSONModel("database.json")


"""
{'id': '5df9eba6-2c6a-4c5f-911c-2c0d650277b5', 'message': {'account_sid': 'ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'api_version': '2010-04-01', 'body': 'Your appointment is coming up on July 21 at 3PM', 'date_created': 'Thu, 24 Aug 2023 05:01:45 +0000', 'date_sent': 'Thu, 24 Aug 2023 05:01:45 +0000', 'date_updated': 'Thu, 24 Aug 2023 05:01:45 +0000', 'direction': 'outbound-api', 'error_code': None, 'error_message': None, 'from': 'whatsapp:+552120420682', 'num_media': '0', 'num_segments': '1', 'price': None, 'price_unit': None, 'messaging_service_sid': 'MGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'sid': 'SMaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'status': 'queued', 'subresource_uris': {'media': '/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Messages/SMaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Media.json'}, 'tags': {'campaign_name': 'Spring Sale 2022', 'message_type': 'cart_abandoned'}, 'to': 'whatsapp:+13233633791', 'uri': '/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Messages/SMaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.json'}}
"""
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
async def read_results(message: Dict[str, Any]):
    id = str(uuid.uuid4())
    data.create({
        "id": id,
        "message": message
    })
    return {
        "success": True,
        "id": id
    }


@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/imgs/ca_icon.ico")


