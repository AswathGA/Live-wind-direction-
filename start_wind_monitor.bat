@echo off
title Wind Monitor Launcher
echo =======================================
echo    Wind Monitor - Automatic Launcher
echo =======================================
echo.
echo Starting Wind Monitor Application...
echo.

REM Change to the wind monitor directory
cd /d "c:\Users\gillxpc\Desktop\wind"

REM Kill any existing Python processes to avoid conflicts
echo Checking for existing Python processes...
taskkill /f /im python.exe 2>nul

REM Wait a moment
timeout /t 2 /nobreak >nul

REM Start the Python wind monitor application in background
echo Starting Python Flask application...
start /B "" ".\.venv\Scripts\python.exe" wind_monitor1.py

REM Wait for the Flask server to start
echo Waiting for server to start...
timeout /t 8 /nobreak >nul

REM Check if the server is running
echo Checking server status...
netstat -an | findstr :5000 >nul
if %errorlevel% equ 0 (
    echo ✓ Flask server is running on port 5000
    echo.
    echo Opening web browser...
    timeout /t 2 /nobreak >nul
    
    REM Open the default browser to the wind monitor
    start "" "http://localhost:5000"
    
    echo.
    echo =======================================
    echo  Wind Monitor is now running!
    echo  Browser should open automatically.
    echo  
    echo  If browser doesn't open, go to:
    echo  http://localhost:5000
    echo.
    echo  Press any key to close this window
    echo  (Wind Monitor will keep running)
    echo =======================================
    pause >nul
) else (
    echo ✗ Failed to start Flask server
    echo.
    echo Troubleshooting:
    echo 1. Make sure all files are in the correct location
    echo 2. Check if the virtual environment exists
    echo 3. Verify log files are accessible
    echo.
    echo Press any key to exit...
    pause >nul
)
