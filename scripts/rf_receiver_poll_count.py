#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
from collections import Counter

DATA_PIN = 5  # Change to your DATA pin
MIN_PULSES = 10  # ignore very short noise
GAP_THRESHOLD = 0.01  # 10 ms gap between packets

GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA_PIN, GPIO.IN)

print("Listening for RF codes (polling + counting)...")
print("Press Ctrl+C to exit.")

last_state = GPIO.input(DATA_PIN)
last_time = time.time()
pulse_times = []
codes_counter = Counter()

def decode_pulses(pulses):
    high_count = len([p for p in pulses if p[0] == 1])
    return high_count

try:
    while True:
        state = GPIO.input(DATA_PIN)
        now = time.time()
        if state != last_state:
            duration = now - last_time
            pulse_times.append((last_state, duration))
            last_state = state
            last_time = now

        # Check for end of packet
        if pulse_times and (now - last_time) > GAP_THRESHOLD:
            if len(pulse_times) >= MIN_PULSES:
                code = decode_pulses(pulse_times)
                codes_counter[code] += 1
                print(f"RF Code: {code} | seen {codes_counter[code]} times | pulses: {len(pulse_times)}")
            pulse_times = []

        time.sleep(0.0001)  # poll fast

except KeyboardInterrupt:
    print("\n--- Summary of codes ---")
    for code, count in codes_counter.most_common():
        print(f"Code: {code} | seen {count} times")
    GPIO.cleanup()
