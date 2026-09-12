from fastapi import FastAPI, Depends
from pydantic import BaseModel
from ai import ask_ai, clear_history, chat_histories
from safety import check_safety
from database import get_contacts
app = FastAPI()

class ClearRequest(BaseModel):
    session_id: str

class Message(BaseModel):
    message: str
    session_id: str
    age: int | None = None
    region: str | None = None
    city: str | None = None

# class PrepareRequest(BaseModel):
#     situation: str
#     person: str
#     mode: str

@app.get("/")
def root():
    return {"status": "API working"}

@app.post("/api/chat")
def chat(data: Message):

    safety = check_safety(data.message)

    answer = ask_ai(
        data.message,
        data.session_id,
        data.age,
        data.region,
        data.city
    )

    return {
        "reply": answer,
        "safety": safety
    }

# @app.post("/api/prepare")
# def prepare(data: PrepareRequest):
#     prompt = f"""
#     Ситуация пользователя:
#     {data.situation}
#
#     С кем он хочет поговорить:
#     {data.person}
#
#     Режим:
#     {data.mode}
#
#     Помоги пользователю подготовиться к разговору.
#     Не добавляй факты, которых пользователь не сообщал.
#     """
@app.post("/api/clear")
def clear(data: ClearRequest):
    clear_history(data.session_id)
    return {"status": "Chat cleared"}

@app.get("/api/contacts")
def contacts(region: str, city: str = ""):
    found_contacts = get_contacts(
        city=city,
        region=region
    )

    return {"contacts": found_contacts}