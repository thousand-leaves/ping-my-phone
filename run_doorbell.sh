#!/bin/bash
# Simple script to run the doorbell system with virtual environment

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the project directory
cd "$SCRIPT_DIR"

# Run the doorbell system using the virtual environment
sudo "$SCRIPT_DIR/venv/bin/python3" "$SCRIPT_DIR/src/doorbell.py"
