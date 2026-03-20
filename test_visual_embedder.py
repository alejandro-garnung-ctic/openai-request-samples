#!/usr/bin/env python3
"""
Prueba el endpoint OpenAI-compatible de embeddings con una imagen (input como data URL).

Uso:
    python scripts/test_embedder_image.py --model Qwen/Qwen3-VL-Embedding-8B --image /ruta/foto.jpg

Variables de entorno (opcional):
    EMBEDDINGS_API_URL   Por defecto: {LITELLM_BASE_URL}
    LITELLM_BASE_URL     Si no hay EMBEDDINGS_API_URL
    LITELLM_API_KEY      Bearer token
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


def _default_embeddings_url() -> str:
    explicit = os.getenv("EMBEDDINGS_API_URL", "").strip()
    if explicit:
        return explicit.rstrip("/")
    endpoint = os.getenv("LITELLM_BASE_URL", "https://litellm.ctic.es").rstrip("/")
    return f"{endpoint}"


def _build_data_url(image_path: Path, jpeg_quality: int | None) -> str:
    raw = image_path.read_bytes()
    if jpeg_quality is not None and jpeg_quality > 0:
        try:
            import io

            from PIL import Image
        except ImportError:
            print(
                "Pillow no instalado: usa --raw o instala pillow para --jpeg-quality",
                file=sys.stderr,
            )
            sys.exit(1)
        im = Image.open(io.BytesIO(raw))
        if getattr(im, "is_animated", False):
            im.seek(0)
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[3])
        buf = io.BytesIO()
        q = min(100, max(1, jpeg_quality))
        bg.save(buf, format="JPEG", quality=q, optimize=True)
        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        return f"data:image/jpeg;base64,{b64}"

    mime = mimetypes.guess_type(image_path.name)[0] or "application/octet-stream"
    b64 = base64.b64encode(raw).decode("utf-8")
    return f"data:{mime};base64,{b64}"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Envía una imagen al endpoint /v1/embeddings (data URL en input).",
    )
    parser.add_argument("--model", required=True, help="Id del modelo en el proxy")
    parser.add_argument("--image", required=True, help="Ruta a la imagen")
    parser.add_argument(
        "--api-url",
        default=None,
        help="URL completa del endpoint embeddings (default: env EMBEDDINGS_API_URL o LITELLM_BASE_URL)",
    )
    parser.add_argument(
        "--token",
        default=None,
        help="Bearer token (default: LITELLM_API_KEY)",
    )
    parser.add_argument(
        "--jpeg-quality",
        type=int,
        default=85,
        metavar="N",
        help="Re-encode a JPEG con calidad N (1-100). Usa 0 para enviar el fichero sin reencode (MIME original). Default: 85",
    )
    args = parser.parse_args()

    path = Path(args.image).expanduser().resolve()
    if not path.is_file():
        print(f"No se encontró la imagen: {path}", file=sys.stderr)
        sys.exit(1)

    url = (args.api_url or _default_embeddings_url()).rstrip("/")
    token = (args.token or os.getenv("LITELLM_API_KEY", "")).strip()

    jq: int | None
    if args.jpeg_quality <= 0:
        jq = None
    else:
        jq = args.jpeg_quality

    data_url = _build_data_url(path, jq)
    body = json.dumps({"model": args.model, "input": data_url}).encode("utf-8")

    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    print(f"POST {url}")
    print(f"model={args.model!r}, input length={len(data_url)} chars (data URL)")

    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            raw_out = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode('utf-8', errors='replace')}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error de red: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(raw_out)
    except json.JSONDecodeError:
        print(raw_out)
        sys.exit(0)

    if "error" in data:
        print(json.dumps(data, indent=2))
        sys.exit(1)

    emb = data.get("data", [{}])[0].get("embedding")
    if emb is None:
        print(json.dumps(data, indent=2))
        sys.exit(1)

    dim = len(emb)
    preview = emb[:8]
    print(f"OK: embedding dim={dim}, primeros valores: {preview} ...")


if __name__ == "__main__":
    main()
