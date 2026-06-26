from openai import OpenAI
from config import OPENAI_API_KEY, MODEL_NAME, TEMPERATURE


client = OpenAI(api_key=OPENAI_API_KEY)


def generate_text(prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=TEMPERATURE,
        messages=[
            {
                "role": "system",
                "content": "You are an expert SEO consultant. Give clear, practical, client-ready recommendations."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content