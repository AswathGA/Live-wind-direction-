@echo off
echo Setting up Git repository for Wind Monitor project...
echo.

REM Navigate to project directory
cd /d "c:\Users\gillxpc\Desktop\wind"

REM Set Git path
set GIT_PATH="C:\Program Files\Git\bin\git.exe"

REM Configure Git user (change email to your actual GitHub email)
echo Configuring Git user...
%GIT_PATH% config --global user.name "AswathGA"
%GIT_PATH% config --global user.email "your-email@example.com"

REM Initialize Git repository
echo Initializing Git repository...
%GIT_PATH% init

REM Add all files
echo Adding all files to Git...
%GIT_PATH% add .

REM Commit with descriptive message
echo Creating initial commit...
%GIT_PATH% commit -m "Initial commit: Professional wind monitoring system with real-time windrose visualization and multi-anemometer support"

REM Set main branch
echo Setting main branch...
%GIT_PATH% branch -M main

REM Add remote origin
echo Adding GitHub remote...
%GIT_PATH% remote add origin https://github.com/AswathGA/Live-wind-direction-.git

REM Push to GitHub
echo Pushing to GitHub...
%GIT_PATH% push -u origin main

echo.
echo Git setup complete!
echo Your wind monitoring project is now on GitHub.
pause
