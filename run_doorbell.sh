#!/bin/bash
# Simple script to run the doorbell system

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the project directory
cd "$SCRIPT_DIR"

# Run the doorbell system using system Python
sudo python3 "$SCRIPT_DIR/src/main.py"
