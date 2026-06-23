@echo off
echo ============================================
echo   Real Rails . PoC #12 . Frontend
echo ============================================
cd /d "%~dp0frontend"
if not exist node_modules (
  echo Installing npm dependencies...
  npm install
)
echo Starting Next.js on http://localhost:3000
npm run dev
pause
