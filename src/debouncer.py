#!/usr/bin/env python3
"""
Debouncer
=========

Encapsulates time-based debouncing logic to prevent rapid repeated events.

This class tracks the last time an event was allowed and ensures a minimum
time interval passes before allowing the next event. 
Useful for preventing notification spam from rapidly repeated button presses
or other events that should be throttled.
"""

import time

class Debouncer:
    def __init__(self, debounce_time=2.0):
        """
        Initialize debouncer with specified debounce time.
        
        Args:
            debounce_time (float): Minimum seconds between allowed events (default: 2.0)
        """
        self.debounce_time = debounce_time
        self.last_allowed_time = 0
    
    def should_allow(self):
        """
        Check if enough time has passed since last allowed event.
        
        Returns True if the debounce time has elapsed since the last call
        that returned True. Automatically updates the last allowed time when
        returning True.
        
        Returns:
            bool: True if event should be allowed, False if still in debounce period
        """
        now = time.time()
        if (now - self.last_allowed_time) >= self.debounce_time:
            self.last_allowed_time = now
            return True
        return False
    
    def reset(self):
        """
        Reset the debouncer to allow immediate next event.
        
        Useful for testing or when you want to manually reset the debounce timer.
        """
        self.last_allowed_time = 0

