from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional, Annotated, Generator
from fastapi import Depends

# ----------------------------
# Define Chat Table Schema
# ----------------------------
class DataChat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    prompt: str
    result: str

# ----------------------------
# Setup SQLite Database
# ----------------------------
DATABASE_FILE = "./db.sqlite3"
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=False)

# Create database and table
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Dependency - Get DB session
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

# Type alias for FastAPI dependency injection
SessionDeps = Annotated[Session, Depends(get_session)]
