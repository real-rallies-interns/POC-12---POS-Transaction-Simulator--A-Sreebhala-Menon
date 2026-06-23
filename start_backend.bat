@echo off
echo ============================================
echo   Real Rails . PoC #12 . Backend
echo ============================================
cd /d "%~dp0backend"
pip install -r requirements.txt
echo Starting FastAPI on http://localhost:8000
uvicorn main:app --reload --host 0.0.0.0 --port 8000
pause
