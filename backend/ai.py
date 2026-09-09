from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "openai/gpt-5.6-luna"
)

def ask_ai(message: str):
    response = client.responses.create(
        model="gpt-5.6-luna",
        instructions="""
Ты — анонимный ИИ-помощник.

Спокойно выслушивай пользователя.
Не осуждай.
Не ставь медицинские диагнозы.
Помогай разобраться в ситуации и подумать о безопасных дальнейших шагах.
""",
        input=message,
        store=False
    )

    return response.output_text