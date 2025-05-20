from machine import Pin, ADC, I2C
import dht
import time
import urequests

# Initialize sensors
dht_sensor = dht.DHT11(Pin(17))  # Indoor temp/humidity
pir_sensor = Pin(19, Pin.IN)      # PIR motion sensor
bathroom_motion = Pin(23, Pin.IN) # Separate bathroom motion
button = Pin(16, Pin.IN, Pin.PULL_UP) # Coffee simulator button
mic_sensor = ADC(Pin(34))         # Simple sound detection

# Time tracking
last_motion_time = time.time()
last_bathroom_use = 0
last_coffee_press = 0

def init():
    """Initialize all sensors"""
    mic_sensor.atten(ADC.ATTN_11DB)
    print("Sensors initialized")

def read_temp_humidity():
    """Read indoor temperature and humidity"""
    try:
        dht_sensor.measure()
        return dht_sensor.temperature(), dht_sensor.humidity()
    except:
        return 20.0, 50.0  # Default values if sensor fails

def read_motion():
    """Check for general motion in living areas"""
    motion = pir_sensor.value()
    if motion:
        global last_motion_time
        last_motion_time = time.time()
    return motion

def read_bathroom_motion():
    """Check for bathroom activity"""
    motion = bathroom_motion.value()
    if motion:
        global last_bathroom_use
        last_bathroom_use = time.time()
    return motion

def read_coffee_button():
    """Check if coffee button was pressed"""
    pressed = not button.value()  # Active low
    if pressed:
        global last_coffee_press
        last_coffee_press = time.time()
    return pressed

def read_sound_level():
    """Get ambient noise level"""
    return mic_sensor.read()

def get_last_motion_duration():
    """Return seconds since last motion was detected"""
    return time.time() - last_motion_time

def get_last_bathroom_use():
    """Return seconds since last bathroom use"""
    return time.time() - last_bathroom_use

def get_last_coffee_press():
    """Return seconds since last coffee button press"""
    return time.time() - last_coffee_press