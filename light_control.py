from machine import Pin, PWM
import time
import math

# Pin definitions
PIN_MAIN_LIGHT = 5    # Main light PWM control
PIN_RGB_STRIP = 14    # Optional RGB strip control (if different from neopixel)

# Constants
MAIN_LIGHT_FREQ = 1000  # PWM frequency for main light

class LightManager:
    def __init__(self):
        """Initialize light control system"""
        # Initialize main light PWM
        self.main_light = PWM(Pin(PIN_MAIN_LIGHT), MAIN_LIGHT_FREQ)
        
        # Sleep schedule parameters (can be customized)
        self.sleep_time = 22 * 3600       # 10 PM (default)
        self.wake_time = 7 * 3600         # 7 AM (default)
        self.dimming_start = 20.5 * 3600  # 8:30 PM (default)
        self.coffee_cutoff = 17 * 3600    # 5 PM (default)
        
        # Set initial brightness to 0
        self.set_brightness(0)
        print("Light manager initialized")
    
    def set_brightness(self, percent):
        """Set main light brightness
        
        Args:
            percent: Brightness level (0-100%)
        """
        # Convert percentage (0-100) to duty cycle (0-1023)
        if not 0 <= percent <= 100:
            percent = max(0, min(100, percent))
        
        duty = int(percent * 10.23)  # Convert % to 0-1023
        self.main_light.duty(duty)
    
    def set_sleep_schedule(self, sleep_hour=22, wake_hour=7, dimming_hour=20.5):
        """Set sleep schedule parameters
        
        Args:
            sleep_hour: Hour to sleep (24-hour format)
            wake_hour: Hour to wake up (24-hour format)
            dimming_hour: Hour to start dimming lights (24-hour format)
        """
        self.sleep_time = sleep_hour * 3600
        self.wake_time = wake_hour * 3600
        self.dimming_start = dimming_hour * 3600
    
    def get_current_time_seconds(self):
        """Get current time of day in seconds
        
        Returns:
            int: Current time in seconds since midnight
        """
        t = time.localtime()
        return t[3] * 3600 + t[4] * 60 + t[5]
    
    def calculate_evening_brightness(self):
        """Calculate appropriate light level based on time before sleep
        
        Returns:
            float: Brightness percentage (0-100)
        """
        current_time = self.get_current_time_seconds()
        
        if current_time < self.dimming_start:
            return 100  # Full brightness
        
        if current_time >= self.sleep_time:
            return 0  # Lights off at sleep time
        
        # Linear dimming from 100% to 0% between dimming start and sleep time
        progress = (current_time - self.dimming_start) / (self.sleep_time - self.dimming_start)
        return max(0, 100 - (progress * 100))
    
    def calculate_morning_brightness(self):
        """Calculate appropriate light level for morning wake-up
        
        Returns:
            float: Brightness percentage (0-100)
        """
        current_time = self.get_current_time_seconds()
        
        # Before wake time, lights off
        if current_time < self.wake_time:
            return 0
        
        # One hour after wake time, full brightness
        wake_end = self.wake_time + 3600
        if current_time >= wake_end:
            return 100
        
        # Linear brightening from 0% to 100% during wake-up hour
        progress = (current_time - self.wake_time) / (wake_end - self.wake_time)
        return min(100, progress * 100)
    
    def simulate_sunrise(self, duration_minutes=30):
        """Gradually increase light for natural wake-up
        
        Args:
            duration_minutes: Duration of sunrise simulation in minutes
        """
        steps = 20  # Number of brightness steps
        delay_seconds = (duration_minutes * 60) / steps  # Time between steps
        
        print(f"Starting sunrise simulation ({duration_minutes} minutes)")
        for i in range(steps + 1):
            brightness = (i / steps) * 100
            self.set_brightness(brightness)
            time.sleep(delay_seconds)
        
        print("Sunrise simulation complete")
    
    def simulate_sunset(self, duration_minutes=30):
        """Gradually decrease light for natural bedtime
        
        Args:
            duration_minutes: Duration of sunset simulation in minutes
        """
        steps = 20  # Number of brightness steps
        delay_seconds = (duration_minutes * 60) / steps  # Time between steps
        
        print(f"Starting sunset simulation ({duration_minutes} minutes)")
        for i in range(steps + 1):
            brightness = 100 - (i / steps) * 100
            self.set_brightness(brightness)
            time.sleep(delay_seconds)
        
        print("Sunset simulation complete")
    
    def adjust_brightness_for_time(self):
        """Automatically adjust brightness based on time of day
        
        Returns:
            float: Applied brightness level (0-100)
        """
        current_time = self.get_current_time_seconds()
        
        # Evening dimming
        if self.dimming_start <= current_time < self.sleep_time:
            brightness = self.calculate_evening_brightness()
            self.set_brightness(brightness)
            return brightness
        
        # Sleep time
        elif current_time >= self.sleep_time or current_time < self.wake_time:
            self.set_brightness(0)
            return 0
        
        # Morning wake-up
        elif self.wake_time <= current_time < self.wake_time + 3600:
            brightness = self.calculate_morning_brightness()
            self.set_brightness(brightness)
            return brightness
        
        # Daytime - full brightness
        else:
            self.set_brightness(100)
            return 100
    
    def lights_on(self, brightness=100):
        """Turn lights on to specified brightness
        
        Args:
            brightness: Brightness level (0-100%)
        """
        self.set_brightness(brightness)
    
    def lights_off(self):
        """Turn lights off"""
        self.set_brightness(0)
    
    def _test_cycle(self):
        """Test function to cycle through brightness levels"""
        print("Running light test cycle")
        # Fade up
        for i in range(0, 101, 5):
            self.set_brightness(i)
            print(f"Brightness: {i}%")
            time.sleep(0.2)
        
        time.sleep(1)
        
        # Fade down
        for i in range(100, -1, -5):
            self.set_brightness(i)
            print(f"Brightness: {i}%")
            time.sleep(0.2)

# For backward compatibility with old code
def init():
    """Initialize lighting system (legacy function)"""
    global main_light
    main_light = PWM(Pin(PIN_MAIN_LIGHT), MAIN_LIGHT_FREQ)
    set_brightness(0)
    print("Light control initialized")

def set_brightness(percent):
    """Set main light brightness (0-100%) (legacy function)"""
    duty = int(percent * 10.23)  # Convert % to 0-1023
    main_light.duty(duty)

def calculate_evening_brightness():
    """Calculate appropriate light level based on time before sleep (legacy function)"""
    current_time = time.localtime()[3] * 3600 + time.localtime()[4] * 60  # Hours and minutes in seconds
    
    if current_time < LIGHT_DIMMING_START:
        return 100  # Full brightness
    
    if current_time >= TARGET_SLEEP_TIME:
        return 0  # Lights off
    
    # Linear dimming from 100% to 0% between dimming start and sleep time
    progress = (current_time - LIGHT_DIMMING_START) / (TARGET_SLEEP_TIME - LIGHT_DIMMING_START)
    return max(0, 100 - (progress * 100))

def simulate_sunrise():
    """Gradually increase light for natural wake-up (legacy function)"""
    for i in range(0, 101, 5):  # 0-100% in 5% steps
        set_brightness(i)
        time.sleep(30)  # 30 seconds between steps (~30 minutes total)

# Legacy globals for backward compatibility
TARGET_SLEEP_TIME = 22 * 3600  # 10 PM
TARGET_WAKE_TIME = 7 * 3600    # 7 AM
LIGHT_DIMMING_START = 20.5 * 3600  # 8:30 PM
main_light = None  # Will be initialized when init() is called