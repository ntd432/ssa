from machine import SoftI2C, Pin
from i2c_lcd import I2cLcd
import time

# LCD default address
DEFAULT_I2C_ADDR = 0x27
LCD_ROWS = 2
LCD_COLS = 16

# I2C pins
PIN_SCL = 22
PIN_SDA = 21

class DisplayManager:
    def __init__(self):
        # Initialize SCL/SDA pins with internal pull-up
        scl_pin = Pin(PIN_SCL, Pin.OUT, pull=Pin.PULL_UP)
        sda_pin = Pin(PIN_SDA, Pin.OUT, pull=Pin.PULL_UP)
        
        # Initialize I2C
        self.i2c = SoftI2C(scl=Pin(PIN_SCL), sda=Pin(PIN_SDA), freq=100000)
        
        # Scan for devices (for debugging)
        devices = self.i2c.scan()
        if not devices:
            print("No I2C devices detected! Check connections")
        else:
            print("I2C devices found at:", [hex(addr) for addr in devices])
        
        # Initialize LCD
        try:
            self.lcd = I2cLcd(self.i2c, DEFAULT_I2C_ADDR, LCD_ROWS, LCD_COLS)
            self.lcd.backlight_on()
            self.lcd.clear()
            self.is_connected = True
            print("LCD display initialized")
        except Exception as e:
            print("LCD initialization failed:", e)
            self.is_connected = False
    
    def display_text(self, text, row=0, col=0):
        """Display text at specified position
        Args:
            text: Text to display
            row: Row (0-1)
            col: Column (0-15)
        """
        if not self.is_connected:
            return
            
        try:
            self.lcd.move_to(col, row)
            self.lcd.putstr(text[:LCD_COLS-col])  # Limit to screen width
        except Exception as e:
            print("LCD display error:", e)
    
    def display_two_lines(self, line1, line2):
        """Display two lines of text
        Args:
            line1: Text for first line
            line2: Text for second line
        """
        if not self.is_connected:
            return
            
        try:
            self.lcd.clear()
            self.lcd.move_to(0, 0)
            self.lcd.putstr(line1[:LCD_COLS])
            self.lcd.move_to(0, 1)
            self.lcd.putstr(line2[:LCD_COLS])
        except Exception as e:
            print("LCD display error:", e)
    
    def clear(self):
        """Clear the display"""
        if self.is_connected:
            try:
                self.lcd.clear()
            except Exception as e:
                print("LCD clear error:", e)
    
    def display_sensor_values(self, temp, humidity):
        """Display temperature and humidity values
        Args:
            temp: Temperature in °C
            humidity: Humidity in %
        """
        if not self.is_connected:
            return
            
        try:
            self.lcd.move_to(0, 0)
            self.lcd.putstr(f"Temp: {temp}C")
            self.lcd.move_to(0, 1)
            self.lcd.putstr(f"Humidity: {humidity}%")
        except Exception as e:
            print("LCD display error:", e)
    
    def display_scrolling_text(self, text, row=0, delay=0.3):
        """Display scrolling text on specified row
        Args:
            text: Text to scroll
            row: Row (0-1)
            delay: Delay between scroll steps in seconds
        """
        if not self.is_connected or not text:
            return
            
        try:
            # Add spaces at the end to scroll completely
            padding = " " * LCD_COLS
            full_text = text + padding
            
            for i in range(len(full_text) - LCD_COLS + 1):
                self.lcd.move_to(0, row)
                self.lcd.putstr(full_text[i:i+LCD_COLS])
                time.sleep(delay)
        except Exception as e:
            print("LCD scrolling error:", e)
    
    def backlight_on(self):
        """Turn on LCD backlight"""
        if self.is_connected:
            try:
                self.lcd.backlight_on()
            except Exception as e:
                print("LCD backlight error:", e)
    
    def backlight_off(self):
        """Turn off LCD backlight"""
        if self.is_connected:
            try:
                self.lcd.backlight_off()
            except Exception as e:
                print("LCD backlight error:", e)