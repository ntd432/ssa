import time
import sensor_manager as sm
import actuator_manager as am
import rfid_manager as rm
import display_manager as dm
import light_control as lc
import web_manager as wm

# Sleep schedule constants
SLEEP_TIME = 22 * 3600  # 10 PM
WAKE_TIME = 7 * 3600    # 7 AM
DIMMING_START = 20.5 * 3600  # 8:30 PM
COFFEE_CUTOFF = 17 * 3600  # 5 PM

def initialize_system():
    """Initialize all system components"""
    dm.show_message("Sleep System\nStarting...")
    #sm.init()
    #am.init()
    #rm.init()
    #wm.init()
    #lc.init()
    dm.show_message("System Ready")
    print("Sleep optimization system initialized")

def get_current_time_seconds():
    """Get current time of day in seconds"""
    t = time.localtime()
    return t[3] * 3600 + t[4] * 60 + t[5]

def enforce_sleep_routine():
    """Manage all sleep-related routines"""
    current_time = get_current_time_seconds()
    
    # Evening wind-down routine
    if DIMMING_START <= current_time < SLEEP_TIME:
        handle_evening_winddown(current_time)
    
    # Sleep time enforcement
    elif current_time >= SLEEP_TIME or current_time < WAKE_TIME:
        handle_sleep_time_enforcement(current_time)
    
    # Morning wake-up routine
    elif WAKE_TIME <= current_time < WAKE_TIME + 3600:  # 1 hour after wake time
        handle_morning_routine()

def handle_evening_winddown(current_time):
    """Evening routine to prepare for sleep"""
    # Gradually dim lights
    brightness = lc.calculate_evening_brightness()
    am.set_lights(brightness)
    
    # Reminder to start winding down
    if current_time >= SLEEP_TIME - 1800:  # 30 minutes before sleep
        if sm.read_motion():
            dm.show_message("Prepare for bed\n30 minutes remaining")
            am.buzzer_beep(440, 0.1)
    
    # Check for late coffee
    if sm.read_coffee_button() and current_time > COFFEE_CUTOFF:
        dm.show_message("Late caffeine\nmay affect sleep")
        am.rgb_flash((255, 50, 0))  # Amber warning
        am.buzzer_beep(330, 0.5)

def handle_sleep_time_enforcement(current_time):
    """Enforce sleep time rules"""
    rm.set_sleep_mode(True)
    
    # Turn off all lights and devices
    am.set_lights(0)
    am.tv_off()
    
    # Check for RFID scan (phone check-in)
    if rm.get_last_scan_duration() > 120:  # 2 minutes since last scan
        am.rgb_flash((255, 0, 0), 0.3)  # Faster red flash
        am.buzzer_on(880)
    else:
        am.rgb_off()
        am.buzzer_off()
    
    # Monitor for night activity
    if current_time > SLEEP_TIME + 3600:  # After 11 PM
        if sm.read_bathroom_motion():
            dm.show_message("Late night activity\nTry to sleep")
            am.rgb_flash((0, 0, 100))  # Soft blue
            
        if sm.read_sound_level() > 2000:  # Noise threshold
            dm.show_message("Please keep\nnoise down")
            am.buzzer_beep(220, 0.1)

def handle_morning_routine():
    """Morning wake-up routine"""
    rm.set_sleep_mode(False)
    
    # Natural light simulation
    if get_current_time_seconds() < WAKE_TIME + 1800:  # First 30 minutes
        lc.simulate_sunrise()
        am.open_blinds()
    
    # After wake time, ensure full brightness
    am.set_lights(100)

def main_loop():
    """Main system loop"""
    initialize_system()
    
    while True:
        enforce_sleep_routine()
        
        # Check environmental conditions
        temp, humidity = sm.read_temp_humidity()
        if temp > 24 or humidity > 70:  # Adjust for comfort
            am.fan_on()
        else:
            am.fan_off()
            
        time.sleep(1)

if __name__ == "__main__":
    main_loop()