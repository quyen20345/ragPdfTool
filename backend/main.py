from typing import List, Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Person(BaseModel):
    name: str
    age: int
    age: int

DB: List[Person] = [
    Person(name="Alice", age=30),
    Person(name="Bob", age=25)
]

@app.get("/api")
def read_root():
    return DB


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}