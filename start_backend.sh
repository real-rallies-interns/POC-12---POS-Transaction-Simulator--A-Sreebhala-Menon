#!/usr/bin/env bash
set -e
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Real Rails · PoC #12 · Backend"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
cd "$(dirname "$0")/backend"
if ! command -v python3 &>/dev/null; then echo "Error: python3 not found"; exit 1; fi
if ! python3 -c "import fastapi" &>/dev/null; then
  echo "Installing dependencies..."
  pip install -r requirements.txt
fi
echo "Starting FastAPI on http://localhost:8000"
echo "Docs → http://localhost:8000/docs"
echo ""
uvicorn main:app --reload --host 0.0.0.0 --port 8000
