from machine import UART
import time

# Initialize RFID reader
uart = UART(2, baudrate=9600, rx=16, tx=17)
last_scan_time = 0
sleep_mode = False

def init():
    """Initialize RFID reader"""
    print("RFID reader initialized")

def check_scan():
    """Check for new RFID scans and return True if detected"""
    global last_scan_time
    if uart.any():
        data = uart.read()
        if data:
            last_scan_time = time.time()
            return True
    return False

def get_last_scan_duration():
    """Return seconds since last RFID scan"""
    return time.time() - last_scan_time

def set_sleep_mode(enabled):
    """Enable or disable sleep mode enforcement"""
    global sleep_mode
    sleep_mode = enabled

def is_sleep_mode():
    """Check if sleep mode is active"""
    return sleep_mode