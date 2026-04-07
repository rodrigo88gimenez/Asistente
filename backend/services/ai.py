import requests
import os

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}


PROMPT = """
Actúa como experto en logística y redacción académica.

Analiza el contenido y:
- detecta problemas
- resume ideas
- propone soluciones tipo WMS
- redacta en formato claro tipo tesina

Contenido:
{input}
"""


def generate_response(text):
    payload = {
        "inputs": PROMPT.format(input=text[:1000])
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()

        return result[0]["generated_text"]

    except Exception as e:
        return f"Error IA: {str(e)}"