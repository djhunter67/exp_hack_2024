from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()  # load environment variables from .env file

account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")

client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='whatsapp:+14155238886',
  content_sid='HXb5b62575e6e4ff6129ad7c8efe1f983e',
  content_variables='{"1":"12/1","2":"3pm"}',
  to='whatsapp:+16036822835'
)

print(message.sid)

def main():

    app = FastAPI(
        title="eXp 2024 Hacking",
        description="This is an API endpoint for AI + Twilio",
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
