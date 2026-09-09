from fastapi import FastAPI
from pydantic import BaseModel

from ai import ask_ai

app = FastAPI()

class Message(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "API working"}

@app.post("/api/chat")
def chat(data: Message):
    answer = ask_ai(data.message)
    return {"reply":f"{answer}"}

