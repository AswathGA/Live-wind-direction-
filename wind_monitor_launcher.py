#!/usr/bin/env python3
"""
Wind Monitor Launcher
Automatically starts the wind monitoring system and opens the web browser
"""

import os
import sys
import time
import subprocess
import webbrowser
import socket
from pathlib import Path

def check_port(host='localhost', port=5000, timeout=1):
    """Check if a port is open"""
    try:
        socket.create_connection((host, port), timeout)
        return True
    except socket.error:
        return False

def kill_existing_processes():
    """Kill any existing Python processes"""
    try:
        subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                      capture_output=True, check=False)
        print("Cleared existing Python processes")
    except Exception as e:
        print(f"Note: {e}")

def start_wind_monitor():
    """Start the wind monitor application"""
    
    print("=" * 50)
    print("    Wind Monitor Launcher")
    print("=" * 50)
    print()
    
    # Set working directory
    wind_dir = Path("c:/Users/gillxpc/Desktop/wind")
    if not wind_dir.exists():
        print("ERROR: Wind monitor directory not found!")
        print(f"Expected location: {wind_dir}")
        input("Press Enter to exit...")
        return False
        
    os.chdir(wind_dir)
    print(f"Working directory: {wind_dir}")
    
    # Check for required files
    python_exe = wind_dir / ".venv" / "Scripts" / "python.exe"
    wind_script = wind_dir / "wind_monitor1.py"
    
    if not python_exe.exists():
        print("ERROR: Python virtual environment not found!")
        print(f"Expected: {python_exe}")
        input("Press Enter to exit...")
        return False
        
    if not wind_script.exists():
        print("ERROR: Wind monitor script not found!")
        print(f"Expected: {wind_script}")
        input("Press Enter to exit...")
        return False
    
    print("All required files found")
    
    # Kill existing processes
    print("\nPreparing environment...")
    kill_existing_processes()
    time.sleep(2)
    
    # Start the Flask application
    print("Starting Wind Monitor application...")
    try:
        # Start the process without waiting for it to complete
        process = subprocess.Popen(
            [str(python_exe), "wind_monitor1.py"],
            cwd=wind_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        )
        print("Flask application started")
        
        # Wait for server to start
        print("Waiting for server to initialize...")
        max_wait = 15  # seconds
        wait_time = 0
        
        while wait_time < max_wait:
            if check_port('localhost', 5000):
                print("Flask server is running on port 5000")
                break
            time.sleep(1)
            wait_time += 1
            print(f"   Waiting... ({wait_time}/{max_wait})")
        
        if wait_time >= max_wait:
            print("Server failed to start within timeout")
            print("   Please check the console for errors")
            input("Press Enter to exit...")
            return False
            
        # Open web browser
        print("\nOpening web browser...")
        time.sleep(2)
        
        url = "http://localhost:5000"
        webbrowser.open(url)
        
        print("=" * 50)
        print("Wind Monitor is now running!")
        print()
        print(f"Web interface: {url}")
        print("Monitor your wind data in real-time")
        print()
        print("To stop the application:")
        print("1. Close this window, or")
        print("2. Press Ctrl+C")
        print("=" * 50)
        
        # Keep the launcher running
        try:
            while True:
                if not check_port('localhost', 5000):
                    print("\nServer appears to have stopped")
                    break
                time.sleep(10)  # Check every 10 seconds
        except KeyboardInterrupt:
            print("\nStopping Wind Monitor...")
            process.terminate()
            print("Wind Monitor stopped")
            
        return True
        
    except Exception as e:
        print(f"ERROR starting application: {e}")
        input("Press Enter to exit...")
        return False

if __name__ == "__main__":
    try:
        start_wind_monitor()
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        input("Press Enter to exit...")
    finally:
        print("Goodbye!")
