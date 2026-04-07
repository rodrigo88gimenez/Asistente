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
Actúa como experto en logística y WMS.

Desarrolla una respuesta estructurada:

1. Problema
2. Justificación
3. Propuesta
4. Conclusión

Contenido:
{input}
"""


def generate_response(text):
    if not HF_API_TOKEN:
        return "[ERROR] Falta HF_API_TOKEN"

    payload = {
        "inputs": PROMPT.format(input=text[:500])  # más corto = más estable
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)

        # 🔍 debug útil
        if response.status_code != 200:
            return f"[ERROR HTTP {response.status_code}] {response.text}"

        # 🔁 retry si modelo cargando
        if response.status_code == 503:
            time.sleep(3)
            response = requests.post(API_URL, headers=headers, json=payload)

        # 🔥 intentar parsear JSON seguro
        try:
            result = response.json()
        except:
            return f"[ERROR] Respuesta no JSON: {response.text[:200]}"

        # ✅ respuesta válida
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]

        # ⚠️ respuesta inesperada
        return f"[ERROR HF] {result}"

    except Exception as e:
        return f"[ERROR EXCEPTION] {str(e)}"