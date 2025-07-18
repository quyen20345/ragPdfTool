from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional, Annotated
from fastapi import Depends 

class DataChat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    prompt: str
    result: str

# engine database URL
# https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#create-the-engine:~:text=about%20it%20later.-,Engine%20Database%20URL,-%C2%B6
rel_db_path = "./db.sqlite3"
file_path_sqlite = f"sqlite:///{rel_db_path}"

# engine is an object that handles the communication with the database 
# https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#create-the-engine:~:text=value%20here.-,Create%20the%20Engine,-%C2%B6
engine = create_engine(file_path_sqlite, echo=True) 

# create the tables in the database.
# https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#engine-technical-details:~:text=and%20inline%20errors.-,Create%20the%20Database%20and%20Table,%C2%B6,-Now%20everything%20is
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDeps = Annotated[Session, Depends(get_session)]