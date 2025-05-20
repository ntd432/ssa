from machine import Pin, PWM, I2C
import neopixel
import time

# Initialize actuators
main_lights = PWM(Pin(5), freq=1000)  # Main room lights
buzzer = PWM(Pin(25))
rgb_leds = neopixel.NeoPixel(Pin(14), 4)
blinds_servo = PWM(Pin(18), freq=50)  # Window blinds
fan_relay = Pin(27, Pin.OUT)          # Fan control
tv_relay = Pin(26, Pin.OUT)           # TV power control

def init():
    """Initialize all actuators"""
    set_lights(0)  # Start with lights off
    buzzer_off()
    rgb_off()
    close_blinds()
    fan_off()
    tv_off()
    print("Actuators initialized")

def set_lights(brightness):
    """Set main lights brightness (0-100%)"""
    duty = int(brightness * 10.23)  # Convert % to 0-1023
    main_lights.duty(duty)

def buzzer_on(freq=1000):
    """Turn on buzzer at specified frequency"""
    buzzer.freq(freq)
    buzzer.duty(512)

def buzzer_off():
    """Turn off buzzer"""
    buzzer.duty(0)

def buzzer_beep(freq=880, duration=0.2):
    """Short beep"""
    buzzer_on(freq)
    time.sleep(duration)
    buzzer_off()

def rgb_set(color):
    """Set all RGB LEDs to a color (r,g,b)"""
    for i in range(4):
        rgb_leds[i] = color
    rgb_leds.write()

def rgb_off():
    """Turn off RGB LEDs"""
    rgb_set((0, 0, 0))

def rgb_flash(color, duration=0.5):
    """Flash RGB LEDs once"""
    rgb_set(color)
    time.sleep(duration)
    rgb_off()
    time.sleep(duration)

def open_blinds():
    """Open window blinds"""
    blinds_servo.duty(77)  # 90 degrees position

def close_blinds():
    """Close window blinds"""
    blinds_servo.duty(25)  # 0 degrees position

def fan_on():
    """Turn on fan"""
    fan_relay.value(1)

def fan_off():
    """Turn off fan"""
    fan_relay.value(0)

def tv_on():
    """Turn on TV"""
    tv_relay.value(1)

def tv_off():
    """Turn off TV"""
    tv_relay.value(0)