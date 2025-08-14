"""
Simple Wind Monitor Starter
Double-click this file to start the wind monitoring system
"""
import subprocess
import sys
import os
import webbrowser
import time

def main():
    print("Wind Monitor System Starting...")
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change to the wind monitor directory
    os.chdir(script_dir)
    
    try:
        # Start the wind monitor
        print("Starting wind monitor server...")
        python_exe = os.path.join(script_dir, ".venv", "Scripts", "python.exe")
        wind_script = os.path.join(script_dir, "wind_monitor1.py")
        
        # Start the server in the background
        process = subprocess.Popen([python_exe, wind_script], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Open the browser
        print("Opening web browser...")
        webbrowser.open('http://localhost:5000')
        
        print("Wind Monitor started successfully!")
        print("Browser should open automatically")
        print("Monitor running at: http://localhost:5000")
        print("\nPress Enter to stop the server...")
        
        # Wait for user input
        input()
        
        # Terminate the process
        process.terminate()
        print("Wind Monitor stopped.")
        
    except Exception as e:
        print(f"Error starting wind monitor: {e}")
        print("Press Enter to exit...")
        input()

if __name__ == "__main__":
    main()
