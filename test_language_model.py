#!/usr/bin/env python3
"""
Script de prueba para enviar consultas a cualquier modelo seleccionable
usando método chat completions.

Uso:
    python test_language_model.py --model <nombre_modelo> --prompt "Tu pregunta aquí"
"""

import os
import sys
import argparse
import requests
import dotenv

dotenv.load_dotenv()

API_URL = os.getenv("CHAT_COMPLETIONS_API_URL", "http://localhost:8000/v1/chat/completions")
API_TOKEN = os.getenv("CHAT_COMPLETIONS_API_TOKEN", "")

def chat_completion(model_name: str, prompt: str):
    headers = {
        "Content-Type": "application/json",
    }
    if API_TOKEN:
        headers["Authorization"] = f"Bearer {API_TOKEN}"

    payload = {
        "model": model_name,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 512,
        "temperature": 0.7
    }

    response = requests.post(API_URL, json=payload, headers=headers, timeout=60)
    if response.status_code != 200:
        print(f"ERROR {response.status_code}: {response.text}")
        return None

    data = response.json()

    # Acceso típico a la respuesta en estructura chat completions
    try:
        content = data["choices"][0]["message"]["content"]
        return content
    except Exception as e:
        print(f"Error leyendo la respuesta JSON: {e}")
        print(data)
        return None

def main():
    parser = argparse.ArgumentParser(description="Prueba chat completions con modelo dado")
    parser.add_argument("--model", required=True, help="Nombre del modelo a usar")
    parser.add_argument("--prompt", required=True, help="Texto de consulta para el modelo")

    args = parser.parse_args()

    print(f"Consultando modelo: {args.model}")
    print(f"Prompt:\n{args.prompt}\n")

    result = chat_completion(args.model, args.prompt)

    if result:
        print("Respuesta del modelo:")
        print(result)
    else:
        print("No se recibió respuesta válida")

if __name__ == "__main__":
    main()
