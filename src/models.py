from typing import Annotated

from fastapi import Depends, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine

class MessageBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)


class Message(MessageBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str


class MessagePublic(MessageBase):
    id: int


class MessageCreate(MessageBase):
    secret_name: str


class MessageUpdate(MessageBase):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]



def save_message(session: Session, message: MessageCreate):
    db_message = Message.model_validate(message)
    session.add(db_message)
    session.commit()
    session.refresh(db_message)
    return db_message

def update_a_message(message_id: int, message: MessageUpdate, session: SessionDep):
    message_db = session.get(Message, message_id)
    if not message_db:
        raise HTTPException(status_code=404, detail="Message not found")
    message_data = message.model_dump(exclude_unset=True)
    message_db.sqlmodel_update(message_data)
    session.add(message_db)
    session.commit()
    session.refresh(message_db)
    return message_db

    
