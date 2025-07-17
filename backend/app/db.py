from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional, Annotated
from fastapi import Depends 

class DataChat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    prompt: str
    result: str

rel_db_path = "./db.sqlite3"
file_path_sqlite = f"sqlite:///{rel_db_path}"

engine = create_engine(file_path_sqlite, echo=True)

def create_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDeps = Annotated[Session, Depends(get_session)]