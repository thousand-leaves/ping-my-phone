#!/usr/bin/env python3
"""
GPIO Cleanup Script
Cleans up all GPIO pins and processes
"""

import subprocess
import sys
import os
import signal

# Prefer system RPi.GPIO (0.7.2) over venv version for better compatibility
if '/usr/local/lib/python3.11/dist-packages' not in sys.path:
    sys.path.insert(0, '/usr/local/lib/python3.11/dist-packages')

import RPi.GPIO as GPIO

def cleanup_gpio_pins():
    """Clean up GPIO pins in both BCM and BOARD modes"""
    print("Cleaning up GPIO pins...")
    
    try:
        # Clean up BCM mode
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()
        print("✓ BCM mode cleaned up")
    except Exception as e:
        print(f"BCM cleanup error: {e}")
    
    try:
        # Clean up BOARD mode
        GPIO.setmode(GPIO.BOARD)
        GPIO.cleanup()
        print("✓ BOARD mode cleaned up")
    except Exception as e:
        print(f"BOARD cleanup error: {e}")

def kill_rf_processes(exclude_pid=None):
    """Kill any running RF receiver processes, excluding the specified PID"""
    print("Killing RF receiver processes...")
    
    processes_to_kill = [
        ('rpi-rf_receive', 'RF receiver'),
        ('doorbell', 'Doorbell'),
        ('button_discovery_tool', 'Button discovery')
    ]
    
    for pattern, name in processes_to_kill:
        try:
            # Get all matching PIDs
            result = subprocess.run(['pgrep', '-f', pattern], capture_output=True, text=True)
            if result.returncode == 0:
                pids = [pid.strip() for pid in result.stdout.strip().split('\n') if pid.strip()]
                killed_any = False
                for pid in pids:
                    pid_int = int(pid)
                    # Skip the excluded PID (the calling process)
                    if exclude_pid and pid_int == exclude_pid:
                        continue
                    try:
                        os.kill(pid_int, signal.SIGTERM)
                        print(f"✓ Stopped {name} process (PID {pid})")
                        killed_any = True
                    except (ProcessLookupError, PermissionError):
                        pass  # Process already gone or no permission
                if not killed_any:
                    print(f"No {name.lower()} processes found (excluding caller)")
            else:
                print(f"No {name.lower()} processes found")
        except Exception as e:
            print(f"Error killing {name.lower()} processes: {e}")

def main():
    """Main cleanup function"""
    # Get PID to exclude (if called from another script)
    exclude_pid = None
    if len(sys.argv) > 1:
        try:
            exclude_pid = int(sys.argv[1])
        except ValueError:
            pass
    
    # Only print header if run directly (not when called silently)
    if exclude_pid is None:
        print("=== GPIO Cleanup Script ===")
        print("Cleaning up all GPIO pins and processes...")
    
    kill_rf_processes(exclude_pid)
    cleanup_gpio_pins()
    
    if exclude_pid is None:
        print("✓ All GPIO pins and processes cleaned up!")
        print("You can now run your RF receiver script safely.")

if __name__ == "__main__":
    main()

