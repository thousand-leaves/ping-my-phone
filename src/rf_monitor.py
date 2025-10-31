#!/usr/bin/env python3
"""
RF Monitor
==========

Encapsulates RF device lifecycle management and code detection.

This class removes global state from the doorbell system and provides
a clean interface for RF signal monitoring.
"""

from rpi_rf import RFDevice


class RFMonitor:    
    def __init__(self, gpio_pin):
        """
        Initialize RFMonitor with GPIO pin configuration.
        
        Args:
            gpio_pin (int): GPIO pin number for RF receiver
        """
        self.gpio_pin = gpio_pin
        self.device = None
        self._last_timestamp = None
    
    def start(self):
        """
        Initialize RF device and enable reception.
        
        Creates RFDevice instance and enables RX mode.
        Must be called before check_for_code().
        """
        self.device = RFDevice(self.gpio_pin)
        self.device.enable_rx()
        self._last_timestamp = None
    
    def check_for_code(self):
        """
        Check for newly detected RF code.
        
        Returns the detected code when a new signal is received,
        or None if no new code has been detected since last call.
        Internally tracks timestamps to avoid returning the same
        code multiple times.
        
        Returns:
            int or None: Detected RF code, or None if no new code
        """
        if not self.device:
            return None
        
        # Check if a new RF code was received
        if self.device.rx_code_timestamp != self._last_timestamp:
            self._last_timestamp = self.device.rx_code_timestamp
            return self.device.rx_code
        
        return None
    
    def cleanup(self):
        """
        Clean up RF device and GPIO resources.
        
        Releases GPIO pins so they can be used again.
        Safe to call multiple times.
        """
        if self.device:
            self.device.cleanup()
            self.device = None
        self._last_timestamp = None

