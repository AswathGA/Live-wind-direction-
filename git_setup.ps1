# PowerShell Git Setup Script
Write-Host "Setting up Git repository for Wind Monitor project..." -ForegroundColor Green
Write-Host ""

# Navigate to project directory
Set-Location "c:\Users\gillxpc\Desktop\wind"

# Set Git executable path
$GitPath = "C:\Program Files\Git\bin\git.exe"

try {
    # Configure Git user (change email to your actual GitHub email)
    Write-Host "Configuring Git user..." -ForegroundColor Yellow
    & $GitPath config --global user.name "AswathGA"
    & $GitPath config --global user.email "your-email@example.com"

    # Initialize Git repository
    Write-Host "Initializing Git repository..." -ForegroundColor Yellow
    & $GitPath init

    # Add all files
    Write-Host "Adding all files to Git..." -ForegroundColor Yellow
    & $GitPath add .

    # Commit with descriptive message
    Write-Host "Creating initial commit..." -ForegroundColor Yellow
    & $GitPath commit -m "Initial commit: Professional wind monitoring system with real-time windrose visualization and multi-anemometer support"

    # Set main branch
    Write-Host "Setting main branch..." -ForegroundColor Yellow
    & $GitPath branch -M main

    # Add remote origin
    Write-Host "Adding GitHub remote..." -ForegroundColor Yellow
    & $GitPath remote add origin https://github.com/AswathGA/Live-wind-direction-.git

    # Push to GitHub
    Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
    & $GitPath push -u origin main

    Write-Host ""
    Write-Host "Git setup complete!" -ForegroundColor Green
    Write-Host "Your wind monitoring project is now on GitHub." -ForegroundColor Green
}
catch {
    Write-Host "Error occurred: $($_.Exception.Message)" -ForegroundColor Red
}

Read-Host "Press Enter to continue"
