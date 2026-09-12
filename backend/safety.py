from openai import APIError
from pathlib import Path
from ai import client, MODEL

with open((Path(__file__).parent.parent / "backend" / "safety_prompt.txt"), "r", encoding="utf-8") as file:
    SAFETY_PROMPT = file.read()


def check_safety(message: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SAFETY_PROMPT
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )

    result = response.choices[0].message.content or "normal"

    return result.strip().lower()