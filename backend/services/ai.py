import requests
import os

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}


PROMPT = """
Analiza el siguiente contenido como experto en logística.

1. Detecta problemas
2. Resume ideas
3. Propone soluciones tipo WMS

Contenido:
{input}
"""


def generate_response(text):
    payload = {
        "inputs": PROMPT.format(input=text[:1000])  # limitamos tamaño
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    try:
        result = response.json()
        return result[0]["generated_text"]
    except:
        return f"Error en modelo IA: {response.text}"
