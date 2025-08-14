@echo off
echo Creating desktop shortcut for Wind Monitor...

set "DESKTOP=%USERPROFILE%\Desktop"
set "SHORTCUT=%DESKTOP%\Wind Monitor.lnk"
set "TARGET=c:\Users\gillxpc\Desktop\wind\start_wind_monitor.py"
set "WORKINGDIR=c:\Users\gillxpc\Desktop\wind"
set "PYTHON_EXE=c:\Users\gillxpc\Desktop\wind\.venv\Scripts\python.exe"

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%SHORTCUT%'); $s.TargetPath = '%PYTHON_EXE%'; $s.Arguments = '"%TARGET%"'; $s.WorkingDirectory = '%WORKINGDIR%'; $s.WindowStyle = 1; $s.Save()"

echo Shortcut created on desktop: Wind Monitor.lnk
echo You can now double-click this shortcut to start the Wind Monitor!
pause
