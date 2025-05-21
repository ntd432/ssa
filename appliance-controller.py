from machine import Pin
import time
from mfrc522_i2c import MFRC522
from i2c_lcd import I2cLcd
from machine import I2C

# Setup
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)
rfid = MFRC522(i2c, 0x28)

# Devices
RED_LED = Pin(17, Pin.OUT)
BUZZER = Pin(18, Pin.OUT)
LIGHT = Pin(19, Pin.OUT)
FAN = Pin(20, Pin.OUT)
COFFEE = Pin(21, Pin.OUT)
DOOR_LOCK = Pin(23, Pin.OUT)
WINDOW_LOCK = Pin(25, Pin.OUT)

BEDTIME_UID = "123456789"  # Replace with phone RFID UID

def turn_off_appliances():
    LIGHT.off()
    FAN.off()
    COFFEE.off()

def activate_locks():
    DOOR_LOCK.on()
    WINDOW_LOCK.on()

def bedtime_alert():
    lcd.clear()
    lcd.putstr("Go to bed!")
    RED_LED.on()
    BUZZER.on()
    print("Bedtime alert active")

def stop_alert():
    RED_LED.off()
    BUZZER.off()

def night_mode():
    turn_off_appliances()
    activate_locks()
    lcd.clear()
    lcd.putstr("Night Mode")
    print("Night mode activated")

def check_rfid():
    if not rfid.card_present():
        return None
    uid = rfid.read_uid()
    if not uid:
        return None
    return "".join([str(b) for b in uid])

# Main logic
bedtime_triggered = False

while True:
    hour = time.localtime()[3]  # Current hour (24h format)

    if hour >= 22 and not bedtime_triggered:
        bedtime_alert()
        bedtime_triggered = True

    if bedtime_triggered:
        scanned_uid = check_rfid()
        if scanned_uid == BEDTIME_UID:
            stop_alert()
            night_mode()
            bedtime_triggered = False

    time.sleep(1)
