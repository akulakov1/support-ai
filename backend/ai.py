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

chat_history = []
MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "openai/gpt-5.6-luna"
)

CHAT_PROMPT = load_prompt("chat_prompt.txt")
PREPARE_PROMPT = load_prompt("prepare_prompt.txt")


def ask_ai(
    message: str,
    age=None,
    region=None,
    city=None
) -> str:

    context = f"""
Возраст: {age}
Регион: {region}
Город: {city}
"""

    chat_history.append({
        "role": "user",
        "content": message
    })

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": CHAT_PROMPT + context
            }
        ] + chat_history
    )

    answer = response.choices[0].message.content or ""

    chat_history.append({
        "role": "assistant",
        "content": answer
    })

    return answer

def clear_history():
    chat_history.clear()