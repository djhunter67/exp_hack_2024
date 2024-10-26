from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse

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