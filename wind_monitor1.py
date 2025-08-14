import pandas as pd
import numpy as np
import re
import os
import glob
from datetime import datetime
import json
from flask import Flask, render_template, jsonify, send_from_directory
import threading
import time
from pathlib import Path

app = Flask(__name__)

class WindDataProcessor:
    def __init__(self, log_dir_path):
        self.log_dir_path = log_dir_path
        self.current_log_file = None
        self.last_file_position = 0
        self.latest_data = {}
        self.debug_mode = False
        self.live_mode = False
        self.monitoring_thread = None
        print(f"WindDataProcessor initialized")
        print(f"Log directory: {self.log_dir_path}")
        
    def start_live_monitoring(self):
        """Start live monitoring of the log files"""
        self.live_mode = True
        self.monitoring_thread = threading.Thread(target=self._monitor_log_files, daemon=True)
        self.monitoring_thread.start()
        print("Started live log file monitoring")
    
    def _monitor_log_files(self):
        """Monitor log files for new data"""
        while self.live_mode:
            try:
                # Find the latest log file
                latest_log = self._get_latest_log_file()
                if latest_log and latest_log != self.current_log_file:
                    print(f"Switching to new log file: {latest_log}")
                    self.current_log_file = latest_log
                    self.last_file_position = 0
                
                if self.current_log_file and Path(self.current_log_file).exists():
                    current_size = Path(self.current_log_file).stat().st_size
                    
                    if current_size > self.last_file_position:
                        # Read new data
                        with open(self.current_log_file, 'r', encoding='utf-8', errors='ignore') as file:
                            file.seek(self.last_file_position)
                            new_content = file.read()
                            self.last_file_position = file.tell()
                        
                        new_lines = new_content.strip().split('\n')
                        
                        # Process new lines
                        processed_count = 0
                        for line in new_lines:
                            if line.strip():  # Skip empty lines
                                data = self.parse_log_line(line.strip())
                                if data:
                                    key = f"{data['anemometer_id']}_{data['port']}"
                                    self.latest_data[key] = data
                                    processed_count += 1
                                    if self.debug_mode:
                                        print(f"Updated {key}: {data['wind_speed']:.2f} m/s @ {data['wind_direction']:.1f}°")
                        
                        if processed_count > 0 and self.debug_mode:
                            print(f"Processed {processed_count} valid lines")
                
                time.sleep(1)  # Check every second
            except Exception as e:
                print(f"Error in log file monitoring: {e}")
                time.sleep(2)
    
    def _get_latest_log_file(self):
        """Get the most recent log file following the naming convention"""
        if self.debug_mode:
            print(f"Looking for log files in: {self.log_dir_path}")
        log_pattern = os.path.join(self.log_dir_path, "serial_*_combined.log")
        if self.debug_mode:
            print(f"Using pattern: {log_pattern}")
        log_files = glob.glob(log_pattern)
        if self.debug_mode:
            print(f"Found {len(log_files)} log files")
        if log_files:
            # Sort by modification time, newest first
            log_files.sort(key=os.path.getmtime, reverse=True)
            if self.debug_mode:
                print(f"Latest log file: {log_files[0]}")
            return log_files[0]
        if self.debug_mode:
            print("No log files found")
        return None
    
    def stop_live_monitoring(self):
        """Stop live monitoring"""
        self.live_mode = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=2)
        print("Stopped live monitoring")
        
    def parse_log_line(self, line):
        """Parse a single log line and extract wind data"""
        # Updated regex to match the actual log format: [PORT:COM3] instead of [COM3]
        pattern = r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+)\] \[PORT:COM(\d+)\] ([A-Z]),([+-]?\d+\.\d+),([+-]?\d+\.\d+),([+-]?\d+\.\d+),M,(\d{2}),([A-Fa-f0-9]{2})'
        # Remove control characters, strip whitespace and line endings
        line = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', line).strip()
        if self.debug_mode:
            print(f"Trying to parse line: {line}")
            print(f"Line length: {len(line)}, repr: {repr(line)}")
        match = re.search(pattern, line)
        if match:
            if self.debug_mode:
                print(f"Regex matched for line: {line}")
            # Extract matched groups
            timestamp_str = match.group(1)
            port = match.group(2)
            record_type = match.group(3)
            u_vel = float(match.group(4))
            v_vel = float(match.group(5))
            w_vel = float(match.group(6))
            channel = int(match.group(7))
            temp_hex = match.group(8)
            try:
                # Parse the timestamp and convert to datetime
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
                # Calculate wind speed and direction
                wind_speed = np.sqrt(u_vel**2 + v_vel**2 + w_vel**2)
                wind_direction = (np.degrees(np.arctan2(v_vel, u_vel)) + 360) % 360
                temperature = int(temp_hex, 16)
                # Return the extracted and computed data
                return {
                    'timestamp': timestamp,
                    'port': f"COM{port}",
                    'anemometer_id': record_type,
                    'u_component': u_vel,
                    'v_component': v_vel,
                    'w_component': w_vel,
                    'wind_speed': wind_speed,
                    'wind_direction': wind_direction,
                    'temperature': temperature,
                    'channel': channel
                }
            except Exception as e:
                print(f"Error processing parsed data: {e}")
                return None
        else:
            # Only show ignored lines if they contain wind data patterns (not status messages)
            if any(x in line for x in [',+', ',-', ',M,']):
                if self.debug_mode:
                    print(f"Ignored line (no match): {line}")
        return None
    
    def read_new_data(self):
        """Read new data from the log file since last read"""
        try:
            with open(self.log_file_path, 'r', encoding='utf-8') as file:
                file.seek(self.last_file_position)
                new_lines = file.readlines()
                self.last_file_position = file.tell()
                
                if self.debug_mode and new_lines:
                    print(f"Read {len(new_lines)} new lines from log file")
                    print(f"First new line: {new_lines[0].strip()}")
                    print(f"Last new line: {new_lines[-1].strip()}")
                
                for line in new_lines:
                    line = line.strip()
                    if line and '[COM' in line:
                        data = self.parse_log_line(line)
                        if data:
                            # Store latest data for each anemometer
                            key = f"{data['port']}_{data['anemometer_id']}"
                            self.latest_data[key] = data
                            if self.debug_mode:
                                print(f"Stored data for {key} - Speed:{data['wind_speed']:.2f} m/s, Direction:{data['wind_direction']:.1f}°")
                            
        except FileNotFoundError:
            print(f"Log file not found: {self.log_file_path}")
        except Exception as e:
            print(f"Error reading log file: {e}")
    
    def read_all_data(self):
        """Read ALL data from the beginning of the file"""
        print("Reading all data from the beginning of the log file...")
        self.last_file_position = 0
        self.latest_data = {}
        
        try:
            with open(self.log_file_path, 'r', encoding='utf-8') as file:
                all_lines = file.readlines()
                self.last_file_position = file.tell()
                
                if self.debug_mode:
                    print(f"Total lines in file: {len(all_lines)}")
                
                parsed_count = 0
                for line_num, line in enumerate(all_lines, 1):
                    line = line.strip()
                    if line and '[COM' in line:
                        data = self.parse_log_line(line)
                        if data:
                            parsed_count += 1
                            # Store latest data for each anemometer
                            key = f"{data['port']}_{data['anemometer_id']}"
                            self.latest_data[key] = data
                            # Show progress for first few entries
                            if self.debug_mode and (parsed_count <= 5 or parsed_count % 100 == 0):
                                print(f"Line {line_num}: {key} - Speed:{data['wind_speed']:.2f} m/s, Direction:{data['wind_direction']:.1f}°")
                
                print(f"Parsed {parsed_count} total wind data entries")
                print(f"Found {len(self.latest_data)} unique anemometers")
                
                if self.debug_mode:
                    for key, data in self.latest_data.items():
                        print(f"   {key}: Latest speed {data['wind_speed']:.2f} m/s, direction {data['wind_direction']:.1f}°")
                            
        except FileNotFoundError:
            print(f"Log file not found: {self.log_file_path}")
        except Exception as e:
            print(f"Error reading log file: {e}")
    
    def get_latest_data(self):
        """Get the latest wind data for all anemometers"""
        return self.latest_data

# Global wind data processor
wind_processor = None

def update_data_continuously():
    """Background thread to continuously update wind data"""
    update_count = 0
    while True:
        if wind_processor:
            if wind_processor.debug_mode:
                print(f"Updating data... ({update_count + 1})")
            wind_processor.read_new_data()
            update_count += 1
            time.sleep(5)

@app.route('/')
def index():
    """Render the home page"""
    return render_template('index.html')

@app.route('/api/wind_data')
def api_wind_data():
    """API endpoint to return the latest wind data"""
    if wind_processor:
        raw_data = wind_processor.get_latest_data()
        
        # Convert datetime objects to ISO format strings for JSON serialization
        formatted_data = {}
        for key, anemometer_data in raw_data.items():
            formatted_data[key] = {
                'anemometer_id': anemometer_data['anemometer_id'],
                'speed': round(anemometer_data['wind_speed'], 2),
                'direction': round(anemometer_data['wind_direction'], 1),
                'u': round(anemometer_data['u_component'], 2),
                'v': round(anemometer_data['v_component'], 2),
                'w': round(anemometer_data['w_component'], 2),
                'temperature': anemometer_data['temperature'],  # Keep as decimal value
                'timestamp': anemometer_data['timestamp'].strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Format with milliseconds
            }
        
        response = {
            'success': True,
            'data': formatted_data,
            'connection_active': len(formatted_data) > 0,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        }
        return jsonify(response)
    return jsonify({
        'success': False,
        'data': {},
        'connection_active': False,
        'error': 'No data available'
    })

@app.route('/logs/<filename>')
def serve_logs(filename):
    """Serve log files"""
    return send_from_directory('logs', filename)

if __name__ == '__main__':
    # Initialize processor with log file path
    log_file_path = r'C:\Users\gillxpc\Desktop\logs'
    print(f"Starting Wind Monitor")
    print(f"Looking for logs in: {log_file_path}")
    print(f"Directory exists: {os.path.exists(log_file_path)}")
    if os.path.exists(log_file_path):
        print(f"Directory contents: {len(os.listdir(log_file_path))} files")
    
    wind_processor = WindDataProcessor(log_file_path)
    # Start live data monitoring
    wind_processor.start_live_monitoring()
    # Run Flask app
    app.run(debug=False, host='0.0.0.0', port=5000)
