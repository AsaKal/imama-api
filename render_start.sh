#!/usr/bin/env bash
set -e

# Download NLTK data needed by LangChain document loaders
python -m nltk.downloader punkt

# Start the FastAPI server
exec uvicorn api:app --host 0.0.0.0 --port "${PORT:-8000}"
