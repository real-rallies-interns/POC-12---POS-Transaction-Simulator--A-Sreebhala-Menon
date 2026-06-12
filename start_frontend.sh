#!/usr/bin/env bash
set -e
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Real Rails · PoC #12 · Frontend"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
cd "$(dirname "$0")/frontend"
if ! command -v node &>/dev/null; then echo "Error: node not found"; exit 1; fi
if [ ! -d node_modules ]; then
  echo "Installing npm dependencies..."
  npm install
fi
echo "Starting Next.js on http://localhost:3000"
echo ""
npm run dev
