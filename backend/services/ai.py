import requests
import os
import time

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}


PROMPT = """
Actúa como experto en logística y redacción académica.

Desarrolla una respuesta completa, estructurada como tesina.

Incluye:
- Problema
- Justificación
- Marco teórico
- Propuesta WMS
- Conclusión

Contenido:
{input}
"""


def call_model(payload):
    return requests.post(API_URL, headers=headers, json=payload)


def generate_response(text):
    if not HF_API_TOKEN:
        return "[ERROR] Falta HF_API_TOKEN en Render"

    payload = {
        "inputs": PROMPT.format(input=text[:800])  # reducimos tamaño
    }

    try:
        response = call_model(payload)

        # 🔁 retry si está cargando modelo
        if response.status_code == 503:
            time.sleep(3)
            response = call_model(payload)

        result = response.json()

        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]

        return f"[ERROR HF] {result}"

    except Exception as e:
        return f"[ERROR EXCEPTION] {str(e)}"