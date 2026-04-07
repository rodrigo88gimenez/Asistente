from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROMPT = """
Actúa como experto en logística y redacción académica.

Analiza el contenido y:
- detecta problemas
- resume ideas
- propone soluciones
- genera texto tipo tesina

Contenido:
{input}
"""


def generate_response(text):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": PROMPT.format(input=text)}
        ]
    )

    return response.choices[0].message.content
