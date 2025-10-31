#!/usr/bin/env python3
"""
Doorbell Service
================

Main service class that encapsulates the doorbell monitoring loop and lifecycle.

This class centralizes the application logic for:
- Monitoring RF signals for button presses
- Debouncing notifications to prevent spam
- Managing the service lifecycle (start/run/stop)
"""

import time

from debouncer import Debouncer


class DoorbellService:
    def __init__(self, config, notifier, rf_monitor, debounce_time=2.0):
        """
        Initialize doorbell service with dependencies.
        
        Args:
            config: DoorbellConfig instance with button_code
            notifier: TelegramNotifier instance for sending notifications
            rf_monitor: RFMonitor instance for detecting RF signals
            debounce_time (float): Minimum seconds between notifications (default: 2.0)
        """
        self.config = config
        self.notifier = notifier
        self.rf_monitor = rf_monitor
        self.debouncer = Debouncer(debounce_time=debounce_time)
    
    def start(self):
        """
        Initialize and start the RF monitor.
        
        This sets up the RF device and enables reception mode.
        """
        self.rf_monitor.start()
    
    def run(self):
        """
        Main monitoring loop.
        
        Continuously polls the RF monitor for new button presses and sends
        notifications when the configured button is detected, subject to debouncing.
        
        This method runs indefinitely until interrupted.
        """
        # Main detection loop
        while True:
            # Check if a new RF code was received
            code = self.rf_monitor.check_for_code()
            
            # Only send notification for our configured button code
            if code == self.config.button_code:
                # Check debouncer to prevent spam
                if self.debouncer.should_allow():
                    self.notifier.notify_doorbell()
            
            time.sleep(0.01)
    
    def stop(self):
        """
        Stop the service and cleanup resources.
        
        Releases RF monitor and GPIO resources.
        """
        self.rf_monitor.cleanup()

