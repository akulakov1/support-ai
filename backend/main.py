from fastapi import FastAPI, Depends
from pydantic import BaseModel
from ai import ask_ai, clear_history, chat_histories
from safety import check_safety
from database import get_contacts
from pathlib import Path
from fastapi.staticfiles import StaticFiles

app = FastAPI()

frontend_folder = Path(__file__).parent.parent / "frontend"

app.mount(
    "/site",
    StaticFiles(directory=frontend_folder),
    name="site"
)

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
    safety_level = check_safety(data.message)

    found_contacts = []

    if data.region:
        found_contacts = get_contacts(
            city=data.city or "",
            region=data.region
        )

    reply = ask_ai(
        message=data.message,
        session_id=data.session_id,
        age=data.age,
        region=data.region,
        city=data.city
    )

    return {
        "reply":reply,
        "safety": safety_level,
        "contacts": found_contacts
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