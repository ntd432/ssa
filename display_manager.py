from machine import I2C, Pin
from i2c_lcd import I2cLcd

DEFAULT_I2C_ADDR = 0x27
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

sleep_messages = [
    "Time to wind down",
    "Lights dimming for sleep",
    "Please prepare for bed",
    "Digital detox time"
]

def init():
    """Initialize the LCD display"""
    lcd.clear()
    lcd.backlight_on()
    print("LCD display initialized")

def show_message(message, priority=1):
    """Display a message with priority handling"""
    # In this simple implementation, we'll just show the message
    lcd.clear()
    lcd.move_to(0, 0)
    if "\n" in message:
        parts = message.split("\n")
        lcd.putstr(parts[0])
        if len(parts) > 1:
            lcd.move_to(0, 1)
            lcd.putstr(parts[1])
    else:
        lcd.putstr(message)

def show_sleep_message(index):
    """Show a pre-defined sleep-related message"""
    if 0 <= index < len(sleep_messages):
        show_message(sleep_messages[index])