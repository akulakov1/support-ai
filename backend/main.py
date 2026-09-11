from fastapi import FastAPI, Depends
from pydantic import BaseModel
from ai import ask_ai, clear_history

app = FastAPI()

class Message(BaseModel):
    message: str
    age: int | None = None
    region: str | None = None
    city: str | None = None

class PrepareRequest(BaseModel):
    situation: str
    person: str
    mode: str

@app.get("/")
def root():
    return {"status": "API working"}

@app.post("/api/chat")
def chat(data: Message):
    answer = ask_ai(
        data.message,
        data.age,
        data.region,
        data.city
    )

    return {"reply": answer}

@app.post("/api/prepare")
def prepare(data: PrepareRequest):
    prompt = f"""
    Ситуация пользователя:
    {data.situation}

    С кем он хочет поговорить:
    {data.person}

    Режим:
    {data.mode}

    Помоги пользователю подготовиться к разговору.
    Не добавляй факты, которых пользователь не сообщал.
    """
@app.post("/api/clear")
def clear():
    clear_history()

    return {
        "status": "Chat cleared"
    }