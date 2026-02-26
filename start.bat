@echo off
echo Starting Workplace Activity Analytics System...
echo.

echo Installing dependencies...
py -m pip install -r requirements.txt

echo.
echo Starting backend server...
start cmd /k "cd backend && py main.py"

echo.
echo Waiting for server to start...
timeout /t 5

echo.
echo Starting frontend server...
start cmd /k "cd frontend && py -m http.server 3000"

echo.
echo Opening dashboard...
timeout /t 2
start http://localhost:3000/dashboard.html

echo.
echo System is running!
echo Backend: http://localhost:8000
echo Dashboard: http://localhost:3000/dashboard.html
echo.
echo Press any key to exit...
pause
