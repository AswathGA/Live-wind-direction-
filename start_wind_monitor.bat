@echo off
setlocal enableextensions enabledelayedexpansion

REM Change to the directory of this script
pushd "%~dp0"

REM Determine Python to use: prefer local venv if available
set "VENV_PY=.venv\Scripts\python.exe"
if exist "%VENV_PY%" (
	set "PYTHON=%VENV_PY%"
) else (
	set "PYTHON=python"
)

echo Starting Wind Monitor using: %PYTHON%

REM Start the Flask app
start "Wind Monitor" "%PYTHON%" "%~dp0wind_monitor1.py"

REM Give the server a moment to start
timeout /t 3 /nobreak >nul

REM Open default browser to the app
start "" http://127.0.0.1:5000/

popd
endlocal
