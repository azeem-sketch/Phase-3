@echo off
echo Cleaning up existing processes...
taskkill /F /IM node.exe /T 2>nul
taskkill /F /IM python.exe /T 2>nul

echo Starting Evolution of Todo...

start cmd /k "echo Starting Backend... && cd evolution-of-todo\backend && venv\Scripts\python run_server.py"
start cmd /k "echo Starting Frontend... && cd evolution-of-todo\frontend && npm run dev -- -H 127.0.0.1"

echo Both servers are starting in separate windows.
echo Frontend: http://127.0.0.1:3000
echo Backend:  http://127.0.0.1:8000
echo.
echo If you get 'Connection Refused', please wait 10 seconds and REFRESH (Ctrl + F5).
pause

