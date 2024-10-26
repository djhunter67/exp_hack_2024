from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from twilio.rest import Client

account_sid = 'ACa8a8854a798b8589d2922edff928e5bb'
auth_token = 'fde69572abba08fde04f270d4589c67b'
from dotenv import load_dotenv
import os

load_dotenv()  # load environment variables from .env file

account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")

client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='+18779165060',
  body='TEST MESSAGE',
  to='+18777804236'
)
print(message.sid)

def main():

app = FastAPI(
    title="Test TREX 2",
    description="This is a testing web app for TREX 2",
    version="0.1.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"request": request}
    )


@app.get("/results/{result_id}")
async def read_results(result_id):
    return {"identified": result_id}


@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/imgs/ca_icon.ico")
