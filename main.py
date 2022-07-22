"""
Demo
"""
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    """Read root"""
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    """Read item"""
    return {"item_id": item_id, "q": q}
