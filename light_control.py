import time
import math
from machine import Pin, PWM

MAIN_LIGHT_PIN = 5
RGB_PIN = 14
MAIN_LIGHT_FREQ = 1000

main_light = PWM(Pin(MAIN_LIGHT_PIN), MAIN_LIGHT_FREQ)

# Sleep schedule
TARGET_SLEEP_TIME = 22 * 3600  # 10 PM
TARGET_WAKE_TIME = 7 * 3600    # 7 AM
LIGHT_DIMMING_START = 20.5 * 3600  # 8:30 PM

def init():
    """Initialize lighting system"""
    set_brightness(0)
    print("Light control initialized")

def set_brightness(percent):
    """Set main light brightness (0-100%)"""
    duty = int(percent * 10.23)  # Convert % to 0-1023
    main_light.duty(duty)

def calculate_evening_brightness():
    """Calculate appropriate light level based on time before sleep"""
    current_time = time.localtime()[3] * 3600 + time.localtime()[4] * 60  # Hours and minutes in seconds
    
    if current_time < LIGHT_DIMMING_START:
        return 100  # Full brightness
    
    if current_time >= TARGET_SLEEP_TIME:
        return 0  # Lights off
    
    # Linear dimming from 100% to 0% between dimming start and sleep time
    progress = (current_time - LIGHT_DIMMING_START) / (TARGET_SLEEP_TIME - LIGHT_DIMMING_START)
    return max(0, 100 - (progress * 100))

def simulate_sunrise():
    """Gradually increase light for natural wake-up"""
    for i in range(0, 101, 5):  # 0-100% in 5% steps
        set_brightness(i)
        time.sleep(30)  # 30 seconds between steps (~30 minutes total)