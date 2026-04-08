import requests
import os

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

API_URL = "https://router.huggingface.co/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json"
}


def generate_response(text):
    if not HF_API_TOKEN:
        return "[ERROR] Falta HF_API_TOKEN"

    payload = {
        "model": "meta-llama/Llama-3-8b-instruct",
        "messages": [
            {
                "role": "system",
                "content": "Sos un experto en logística, WMS y redacción académica."
            },
            {
                "role": "user",
                "content": f"""
Desarrollá una respuesta tipo tesina con:

1. Problema
2. Justificación
3. Propuesta de solución WMS
4. Conclusión

Contenido:
{text[:600]}
"""
            }
        ],
        "max_tokens": 500
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code != 200:
            return f"[ERROR HTTP {response.status_code}] {response.text}"

        result = response.json()

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"[ERROR EXCEPTION] {str(e)}"