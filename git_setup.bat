@echo off
echo Setting up Git repository for Wind Monitor project...
echo.

REM Navigate to project directory
cd /d "c:\Users\gillxpc\Desktop\wind"

REM Initialize Git repository
echo Initializing Git repository...
git init

REM Add all files
echo Adding all files to Git...
git add .

REM Commit with descriptive message
echo Creating initial commit...
git commit -m "Initial commit: Professional wind monitoring system with real-time windrose visualization"

REM Set main branch
echo Setting main branch...
git branch -M main

REM Add remote origin
echo Adding GitHub remote...
git remote add origin https://github.com/AswathGA/Live-wind-direction-.git

REM Push to GitHub
echo Pushing to GitHub...
git push -u origin main

echo.
echo Git setup complete!
echo Your wind monitoring project is now on GitHub.
pause
