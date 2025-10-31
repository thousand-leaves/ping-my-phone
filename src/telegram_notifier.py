#!/usr/bin/env python3
"""
Telegram Notifier
=================

Handles sending notifications to Telegram via the Telegram Bot API.
"""

import time
import requests

class TelegramNotifier:    
    def __init__(self, bot_token, chat_id, timeout=5):
        """
        Initialize the Telegram notifier.
        
        Args:
            bot_token: Telegram bot token from BotFather
            chat_id: Telegram chat ID to send notifications to
            timeout: Request timeout in seconds (default: 5)
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.timeout = timeout
        self.api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    def notify_doorbell(self):
        """
        Send doorbell notification to Telegram.
        
        Handles errors gracefully - logs warnings but doesn't crash the application
        if the notification fails to send.
        """
        try:
            message = f"🔔 DOORBELL PRESSED! 🔔\nTime: {time.strftime('%H:%M:%S')}"
            response = requests.post(
                self.api_url,
                data={"chat_id": self.chat_id, "text": message},
                timeout=self.timeout
            )
            response.raise_for_status()  # Raise exception if HTTP error
            print(f"✅ Notification sent!")
        except Exception as e:
            print(f"⚠️ Warning: Failed to send notification: {e}")
            # Don't crash - just log the error and continue running

