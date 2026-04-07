import requests
import os
import time

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

API_URL = "https://router.huggingface.co/hf-inference/models/google/flan-t5-base"

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json"
}


PROMPT = """
Actúa como experto en logística, sistemas WMS y redacción académica.

Desarrolla una respuesta estructurada tipo tesina con:

1. Definición del problema
2. Justificación
3. Propuesta de solución WMS
4. Conclusión

Contenido:
{input}
"""


def call_model(payload):
    return requests.post(API_URL, headers=headers, json=payload)


def generate_response(text):
    if not HF_API_TOKEN:
        return "[ERROR] Falta configurar HF_API_TOKEN en Render"

    payload = {
        "inputs": PROMPT.format(input=text[:800])
    }

    try:
        response = call_model(payload)

        # 🔁 retry si el modelo está cargando
        if response.status_code == 503:
            time.sleep(3)
            response = call_model(payload)

        result = response.json()

        # respuesta válida
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]

        # error de HuggingFace
        return f"[ERROR HF] {result}"

    except Exception as e:
        return f"[ERROR EXCEPTION] {str(e)}"