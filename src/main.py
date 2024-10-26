from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from modeles import create_db_and_tables, save_message, update_message, Message, MessageCreate, MessageUpdate, MessagePublic, SessionDep, Annotated, select

app = FastAPI(
    title="eXp 2024 Hacking",
    description="This is an API endpoint for AI + Twilio",
    version="0.1.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request, session: SessionDep):
    # Get all the messages from the database
    messages = session.exec(select(Message)).all()
    return templates.TemplateResponse(
        request=request, name="index.html", context={"request": request, "messages": messages}
    )


@app.post("/twilio/whatsapp")
async def read_results(message: Message):
    save_message(message)
    return message


@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/imgs/ca_icon.ico")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/messagees/", response_model=MessagePublic)
def create_message(message: MessageCreate, session: SessionDep):
    return save_message(session, message)


@app.get("/messagees/", response_model=list[MessagePublic])
def read_messagees(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    messagees = session.exec(select(Message).offset(offset).limit(limit)).all()
    return messagees


@app.get("/messagees/{message_id}", response_model=MessagePublic)
def read_message(message_id: int, session: SessionDep):
    message = session.get(Message, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message


@app.patch("/messagees/{message_id}", response_model=MessagePublic)
def update_a_message(message_id: int, message: MessageUpdate, session: SessionDep):
    return update_message(message_id, message, session)

@app.delete("/messagees/{message_id}")
def delete_message(message_id: int, session: SessionDep):
    message = session.get(Message, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    session.delete(message)
    session.commit()
    return {"ok": True}

