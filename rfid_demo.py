"""
Filename: RFID
Description: RFID reader UID
Author: http://www.keyestudio.com
Ported to Python by: GitHub Copilot
"""
from machine import I2C, Pin, PWM
from i2c_lcd import I2cLcd
from mfrc522_i2c import MFRC522
import time

# Initialize I2C
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)

# Initialize LCD (I2C address 0x27)
lcd = I2cLcd(i2c, 0x27, 2, 16)

# Initialize RFID reader (I2C address 0x28)
rfid = MFRC522(i2c, 0x28)

# Define pins
SERVO_PIN = 13
BTN_PIN = 16

# Set up button as input with pull-up
btn = Pin(BTN_PIN, Pin.IN, Pin.PULL_UP)

# Set up servo
servo = PWM(Pin(SERVO_PIN))
servo.freq(50)  # 50Hz frequency for servo

# Constants for servo control
SERVO_MIN = 40    # 0 degrees (1ms pulse)
SERVO_MAX = 115   # 180 degrees (2ms pulse)

btn_flag = False
password = ""

def servo_write(angle):
    """Set servo angle between 0-180 degrees"""
    # Scale angle to duty cycle (40-115)
    duty = int(SERVO_MIN + (SERVO_MAX - SERVO_MIN) * angle / 180)
    servo.duty(duty)

def show_reader_details():
    """Display MFRC522 version information"""
    version = rfid.read_version()
    print(f"MFRC522 Software Version: 0x{version:02X}")
    
    if version == 0x91:
        print(" = v1.0")
    elif version == 0x92:
        print(" = v2.0")
    else:
        print(" (unknown)")
    
    if version == 0x00 or version == 0xFF:
        print("WARNING: Communication failure, is the MFRC522 properly connected?")

def init():
    """Initialize the system"""
    # Initialize LCD
    lcd.clear()
    lcd.backlight_on()
    
    # Show initial message
    lcd.move_to(0, 0)
    lcd.putstr("Card")
    
    # Initialize RFID
    rfid.init()
    show_reader_details()
    print("Scan PICC to see UID, type, and data blocks...")
    
    # Set servo to initial position
    servo_write(0)

def main_loop():
    """Main program loop"""
    global btn_flag, password
    
    while True:
        # Check if a new card is present
        if not rfid.card_present():
            time.sleep(0.05)
            password = ""
            
            # Check button if door is open
            if btn_flag:
                if not btn.value():  # Button is pressed (active low)
                    print("close")
                    lcd.clear()
                    lcd.move_to(0, 0)
                    lcd.putstr("close")
                    servo_write(0)
                    btn_flag = False
            continue

        # Read card UID
        uid = rfid.read_uid()
        if not uid:
            continue

        # Display UID
        print("Card UID:", end="")
        password = ""
        for byte in uid:
            print(f" {byte}", end="")
            password += str(byte)
        print()

        # Replace with your actual card UID
        if password == "123456789":  # Example UID - replace with your card's actual UID
            print("open")
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr("open")
            servo_write(180)
            password = ""
            btn_flag = True
        else:
            password = ""
            lcd.move_to(0, 0)
            lcd.putstr("error")
        
        # Small delay to prevent reading the same card multiple times
        time.sleep(0.5)

if __name__ == "__main__":
    init()
    main_loop()