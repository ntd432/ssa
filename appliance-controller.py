# Smart Home Appliance Controller for Raspberry Pi Pico
# Auto-controls appliances based on motion and time
 
from machine import Pin, Timer
import time
 
# Initialize appliance control pins (connect to relays)
appliances = {
    "living_room_light": Pin(16, Pin.OUT, value=1),  # ON by default
    "tv": Pin(17, Pin.OUT, value=1),
    "coffee_maker": Pin(18, Pin.OUT, value=1),
    "ac": Pin(19, Pin.OUT, value=1)
}
 
# Motion sensor setup (PIR sensor on GPIO 20)
motion_sensor = Pin(20, Pin.IN)
last_motion_time = time.time()
 
# Essential devices (not in appliance list since they should never be turned off)
ESSENTIAL_DEVICES = []
 
# Callback when motion is detected
def check_motion(pin):
    global last_motion_time
    last_motion_time = time.time()
    print("Motion detected at", time.localtime())
 
# Attach interrupt to motion sensor
motion_sensor.irq(trigger=Pin.IRQ_RISING, handler=check_motion)
 
# Timer callback to automatically manage appliance shutoff
def auto_shutoff(timer):
    current_time = time.localtime()
    elapsed = time.time() - last_motion_time
 
    # 1. Shut off non-essential appliances if no motion for 30 minutes
    if elapsed > 1800:  # 30 minutes
        for name, pin in appliances.items():
            if name not in ESSENTIAL_DEVICES:
                if pin.value():  # Only print when changing state
                    pin.value(0)
                    print(f"Auto OFF due to inactivity: {name}")
 
    # 2. Shut off AC at 11 PM
    if current_time[3] == 23:  # Hour = 23 (11 PM)
        if appliances["ac"].value():
            appliances["ac"].value(0)
            print("Auto OFF AC at 11 PM")
 
# Set up timer to call auto_shutoff every 5 minutes (300000 ms)
schedule_timer = Timer()
schedule_timer.init(period=300000, mode=Timer.PERIODIC, callback=auto_shutoff)
 
# Idle loop to keep the program running
print("Smart Home Controller running...")
while True:
    time.sleep(1)