@echo off
REM Start the Python server directly
start "Wind Monitor" python wind_monitor1.py
REM Wait a shorter time for the server to start
timeout /t 3 /nobreak >nul
REM Open Chrome to localhost:5000 in a regular tab
start "" "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" http://localhost:5000
