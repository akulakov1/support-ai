from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def load_prompt(filename: str) -> str:
    path = Path(__file__).parent.parent / "backend" / filename
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

chat_histories = {}
MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "openai/gpt-5.6-luna"
)

CHAT_PROMPT = load_prompt("chat_prompt.txt")
PREPARE_PROMPT = load_prompt("prepare_prompt.txt")


def ask_ai(message: str, session_id: str, age=None, region=None, city=None) -> str:

    if session_id not in chat_histories:
        chat_histories[session_id] = []

    history = chat_histories[session_id]

    context = f"""
Возраст: {age}
Регион: {region}
Город: {city}
"""

    history.append({
        "role": "user",
        "content": message
    })

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
             {
                 "role": "system",
                 "content": CHAT_PROMPT
             },
             {
                 "role": "user",
                 "content": "Анкетные данные пользователя:\n" + context
             }
         ] + history
    )

    answer = response.choices[0].message.content or ""

    history.append({
        "role": "assistant",
        "content": answer
    })

    return answer

def clear_history(session_id: str):
    chat_histories[session_id] = []