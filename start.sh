#!/usr/bin/env bash
# Linux / macOS equivalent of start.bat
set -e
cd "$(dirname "$0")"
[ -f .env ] || cp .env.example .env
[ -d backend/venv ] || python3 -m venv backend/venv
backend/venv/bin/pip install -q -r backend/requirements.txt
[ -d frontend/node_modules ] || (cd frontend && npm install --no-audit --no-fund)
(cd backend && venv/bin/python -m uvicorn app.main:app --reload --port 8000) &
BACK=$!
trap "kill $BACK 2>/dev/null" EXIT
cd frontend && npm run dev
