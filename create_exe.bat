@echo off
cd /d "c:\Users\gillxpc\Desktop\wind"
echo Creating Wind Monitor EXE file...
.\.venv\Scripts\python.exe -m PyInstaller --onefile --name "WindMonitorLauncher" wind_monitor_launcher.py
echo.
echo EXE creation complete!
echo The EXE file will be in the 'dist' folder
pause
