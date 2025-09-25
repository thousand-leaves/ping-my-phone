#!/bin/bash
# Doorbell Service Management Script
# Provides easy commands to manage the doorbell systemd service

SERVICE_NAME="doorbell.service"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    case $status in
        "success") echo -e "${GREEN}✅ $message${NC}" ;;
        "error") echo -e "${RED}❌ $message${NC}" ;;
        "warning") echo -e "${YELLOW}⚠️  $message${NC}" ;;
        "info") echo -e "${BLUE}ℹ️  $message${NC}" ;;
    esac
}

# Function to check if service exists
check_service_exists() {
    if ! systemctl list-unit-files | grep -q "$SERVICE_NAME"; then
        print_status "error" "Service $SERVICE_NAME not found. Make sure it's installed."
        exit 1
    fi
}

# Function to show service status
show_status() {
    print_status "info" "Checking doorbell service status..."
    echo
    sudo systemctl status "$SERVICE_NAME" --no-pager
    echo
    print_status "info" "Recent logs:"
    sudo journalctl -u "$SERVICE_NAME" -n 10 --no-pager
}

# Function to start service
start_service() {
    print_status "info" "Starting doorbell service..."
    if sudo systemctl start "$SERVICE_NAME"; then
        print_status "success" "Doorbell service started successfully"
    else
        print_status "error" "Failed to start doorbell service"
        exit 1
    fi
}

# Function to stop service
stop_service() {
    print_status "info" "Stopping doorbell service..."
    if sudo systemctl stop "$SERVICE_NAME"; then
        print_status "success" "Doorbell service stopped successfully"
    else
        print_status "error" "Failed to stop doorbell service"
        exit 1
    fi
}

# Function to restart service
restart_service() {
    print_status "info" "Restarting doorbell service..."
    if sudo systemctl restart "$SERVICE_NAME"; then
        print_status "success" "Doorbell service restarted successfully"
    else
        print_status "error" "Failed to restart doorbell service"
        exit 1
    fi
}

# Function to enable service
enable_service() {
    print_status "info" "Enabling doorbell service to start on boot..."
    if sudo systemctl enable "$SERVICE_NAME"; then
        print_status "success" "Doorbell service enabled for boot"
    else
        print_status "error" "Failed to enable doorbell service"
        exit 1
    fi
}

# Function to disable service
disable_service() {
    print_status "info" "Disabling doorbell service from starting on boot..."
    if sudo systemctl disable "$SERVICE_NAME"; then
        print_status "success" "Doorbell service disabled from boot"
    else
        print_status "error" "Failed to disable doorbell service"
        exit 1
    fi
}

# Function to show logs
show_logs() {
    print_status "info" "Showing doorbell service logs (press Ctrl+C to exit)..."
    sudo journalctl -u "$SERVICE_NAME" -f
}

# Function to show help
show_help() {
    echo "Doorbell Service Management Script"
    echo "=================================="
    echo
    echo "Usage: $0 [COMMAND]"
    echo
    echo "Commands:"
    echo "  start     - Start the doorbell service"
    echo "  stop      - Stop the doorbell service"
    echo "  restart   - Restart the doorbell service"
    echo "  status    - Show service status and recent logs"
    echo "  enable    - Enable service to start on boot"
    echo "  disable   - Disable service from starting on boot"
    echo "  logs      - Show real-time logs (Ctrl+C to exit)"
    echo "  help      - Show this help message"
    echo
    echo "Examples:"
    echo "  $0 start"
    echo "  $0 status"
    echo "  $0 logs"
}

# Main script logic
case "${1:-help}" in
    "start")
        check_service_exists
        start_service
        ;;
    "stop")
        check_service_exists
        stop_service
        ;;
    "restart")
        check_service_exists
        restart_service
        ;;
    "status")
        check_service_exists
        show_status
        ;;
    "enable")
        check_service_exists
        enable_service
        ;;
    "disable")
        check_service_exists
        disable_service
        ;;
    "logs")
        check_service_exists
        show_logs
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        print_status "error" "Unknown command: $1"
        echo
        show_help
        exit 1
        ;;
esac
