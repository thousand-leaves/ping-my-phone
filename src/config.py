#!/usr/bin/env python3
"""
Configuration Management
========================

Handles loading and validating all configuration for the doorbell system.

Configuration Sources:
1. Environment variables (.env file): BOT_TOKEN, CHAT_ID, GPIO_DATA_PIN
2. JSON file (button_config.json): BUTTON_CODE
"""

import json
import os
from dotenv import load_dotenv


class DoorbellConfig:
    def __init__(self):
        """
        Initialize configuration by loading from all sources.
        
        This automatically:
        1. Finds the project root directory
        2. Loads environment variables from .env file
        3. Loads button code from JSON config file
        4. Validates that all required values are present
        """
        self.project_root = self._get_project_root()
        self._load_env_variables()
        self._load_button_config()
        self._validate()
    
    def _get_project_root(self):
        """
        Find the project root directory.

        Returns:
            str: Path to the project root directory
        """
        # Get the directory where this script (config.py) is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level to get the project root (src/ -> project_root/)
        project_root = os.path.dirname(script_dir)
        return project_root
    
    def _load_env_variables(self):
        """
        Load environment variables from .env file.
        
        Loads:
        - BOT_TOKEN: Telegram bot token from BotFather (required)
        - CHAT_ID: Telegram chat ID to send notifications to (required)
        - GPIO_DATA_PIN: GPIO pin number for RF receiver (optional, defaults to 27)
        """
        # Find .env file in project root
        env_file = os.path.join(self.project_root, '.env')
        # Load environment variables from .env file
        load_dotenv(env_file)
        
        # Load configuration values
        # Note: os.getenv() returns None if the variable is not set
        self.bot_token = os.getenv('BOT_TOKEN')
        self.chat_id = os.getenv('CHAT_ID')
        
        # GPIO pin defaults to 27 if not specified
        # int() converts string to integer (e.g., '27' -> 27)
        gpio_pin_str = os.getenv('GPIO_DATA_PIN', '27')
        self.gpio_pin = int(gpio_pin_str)
    
    def _load_button_config(self):
        """
        Load button code from JSON configuration file.
        
        - Button code is discovered by the button_discovery_tool.py
        - Stored separately from .env so it can be updated by the tool
        
        Loads:
        - BUTTON_CODE: The RF code that identifies our specific button
        """
        # Find button_config.json in project root
        config_file = os.path.join(self.project_root, 'button_config.json')
        
        # Open and read the JSON file
        with open(config_file, 'r') as f:
            config_data = json.load(f)
        
        # Extract the button code
        self.button_code = config_data['BUTTON_CODE']
    
    def _validate(self):
        """
        Validate that all required configuration values are present.

        - Prevents runtime errors later when trying to use missing values
        - Gives clear error messages about what's missing
        - Fails fast - catches problems at startup, not during operation
        
        Raises:
            ValueError: If any required configuration is missing
        """
        # Check if required Telegram credentials are set
        if not self.bot_token:
            raise ValueError("BOT_TOKEN must be set in .env file")
        
        if not self.chat_id:
            raise ValueError("CHAT_ID must be set in .env file")
        
        # Note: button_code validation would happen in _load_button_config()
        # if the JSON file is missing or malformed, that will raise an error there

