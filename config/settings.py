"""
Configuration settings for Ping-My-Phone
Loads configuration from .env file in the project root
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN', '')
CHAT_ID = os.getenv('CHAT_ID', '')

# RF Receiver Configuration
RF_RECEIVER_PIN = int(os.getenv('RF_RECEIVER_PIN', '18'))
POLL_INTERVAL = float(os.getenv('POLL_INTERVAL', '0.1'))

# Signal Filtering
ALLOWED_RF_CODES_STR = os.getenv('ALLOWED_RF_CODES', '')
ALLOWED_RF_CODES = [int(code.strip()) for code in ALLOWED_RF_CODES_STR.split(',') if code.strip()]

# Notification Settings
SEND_NOTIFICATIONS = os.getenv('SEND_NOTIFICATIONS', 'true').lower() == 'true'
NOTIFICATION_COOLDOWN = int(os.getenv('NOTIFICATION_COOLDOWN', '5'))
