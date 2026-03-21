# openai-request-sample

Ejemplos de cliente para hacer llamadas a una API compatible con OpenAI Chat Completions.

## Instalación

```bash
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

## Configuración

Variables de entorno:
- `CHAT_COMPLETIONS_API_URL`: URL de la API (default: `http://localhost:8000/v1/chat/completions`)
- `CHAT_COMPLETIONS_API_TOKEN`: Token de autenticación (opcional)

Crea el archivo `.env` con tus variables:

```bash
cp .env.example .env
```

## Modelos disponibles

| Modelo                                            | Tipo / Descripción                                                                 |
| ------------------------------------------------- | ---------------------------------------------------------------------------------- |
| **BAAI/bge-reranker-v2-m3**                       | Modelo **Reranker** (para ordenar resultados, búsquedas)                           |
| **cpatonn/Qwen3-VL-32B-Instruct-AWQ-4bit**        | Modelo multimodal **VL** (Vision + Language), Instruct, 32B parámetros, 4bit quant |
| **input_inspector**                               | Herramienta o modelo para inspección/diagnóstico, no un LLM típico                 |
| **meta-llama/Llama-3-3.3-70B-Instruct**           | Modelo **Llama 3**, 70B parámetros, instructivo (LLM solo texto)                   |
| **mistralai/Magistral-Small-2509**                | Modelo VLLM pequeño
| **mistralai/Ministral-3-14B-Instruct-2512**       | Modelo VLLM pequeño, 14B parámetros
| **mistralai/Mistral-Small-3.2-24B-Instruct-2506** | Modelo VLLM, 24B parámetros
| **openai/gpt-oss-120b**                           | GPT open source, 120B parámetros, solo texto                                       |
| **openai/whisper-large-v3-turbo**                 | Modelo de reconocimiento de voz (ASR), no texto/imagen                             |
| **Qwen/Qwen3-32B**                                | LLM texto solo, 32B parámetros                                                     |
| **Qwen/Qwen3-32B-AWQ**                            | Igual que anterior pero con cuantización AWQ para optimización                     |
| **Qwen/Qwen3-4B**                                 | LLM texto solo, 4B parámetros                                                      |
| **Qwen/Qwen3-8B-AWQ**                             | LLM texto solo, 8B parámetros, AWQ cuantizado                                      |
| **Qwen/Qwen3-Embedding-4B**                       | Modelo para generar embeddings vectoriales, no generación texto                    |
| **Qwen/Qwen3-Reranker-8B**                        | Modelo reranker, para clasificación/ordenación                                     |
| **Qwen/Qwen3-VL-235B-A22B-Instruct**              | Multimodal VL, muy grande (235B+), instructivo                                     |
| **Qwen/Qwen3-VL-32B-Thinking**                    | Multimodal VL 32B parámetros |
| **SmolPiper**                                     | -                        |
| **Snowflake/snowflake-arctic-embed-l-v2.0**       | Modelo embedding para vectores, tipo búsqueda o recomendación                      |

## Uso

### Modelo de lenguaje

```bash
python3 test_language_model.py --model <nombre_modelo> --prompt "Tu pregunta aquí"
```

### Modelo multimodal (con imagen)

```bash
python3 test_multimodal_model.py --model <nombre_modelo> --prompt "Describe la imagen" --image <ruta_imagen>
```

### Modelo de embeddings visuales

```bash
python3 scripts/test_embedder_image.py --model <nombre_modelo> --image <ruta_imagen> --jpeg-quality 75
```
