from machine import Pin, ADC, I2C
import dht
import time

# Pin definitions
PIN_DHT = 17        # DHT11 temperature/humidity sensor
PIN_PIR = 14        # PIR motion sensor
PIN_BTN1 = 16       # Button 1 (with pull-up)
PIN_BTN2 = 27       # Button 2 (with pull-up) 
PIN_GAS = 23        # Gas sensor (from example pj8_2)
PIN_SOUND = 34      # Sound sensor (microphone)

class SensorManager:
    def __init__(self):
        # Initialize all sensors
        self.dht_sensor = dht.DHT11(Pin(PIN_DHT))
        self.pir_sensor = Pin(PIN_PIR, Pin.IN)
        self.button1 = Pin(PIN_BTN1, Pin.IN, Pin.PULL_UP)
        self.button2 = Pin(PIN_BTN2, Pin.IN, Pin.PULL_UP)
        self.gas_sensor = Pin(PIN_GAS, Pin.IN, Pin.PULL_UP)
        self.sound_sensor = ADC(Pin(PIN_SOUND))
        
        # Configure analog sensors
        self.sound_sensor.atten(ADC.ATTN_11DB)  # Full range: 0-3.3V
        
        # Time tracking for events
        self.last_motion_time = 0
        self.last_btn1_press = 0
        self.last_btn2_press = 0
        
        print("Sensor manager initialized")
    
    def read_temperature_humidity(self):
        """Read temperature and humidity from DHT11 sensor
        Returns: (temperature, humidity) in °C and %
        """
        try:
            self.dht_sensor.measure()
            temp = self.dht_sensor.temperature()
            humidity = self.dht_sensor.humidity()
            return (temp, humidity)
        except Exception as e:
            print("DHT sensor error:", e)
            return (0, 0)  # Return defaults on error
    
    def is_motion_detected(self):
        """Check if motion is detected by PIR sensor
        Returns: True if motion detected, False otherwise
        """
        motion = self.pir_sensor.value()
        if motion:
            self.last_motion_time = time.time()
        return bool(motion)
    
    def is_button1_pressed(self):
        """Check if button 1 is pressed (active low)
        Returns: True if pressed, False otherwise
        """
        # Button is active low (0 when pressed)
        pressed = not self.button1.value()
        if pressed:
            self.last_btn1_press = time.time()
        return pressed
    
    def is_button2_pressed(self):
        """Check if button 2 is pressed (active low)
        Returns: True if pressed, False otherwise
        """
        # Button is active low (0 when pressed)
        pressed = not self.button2.value()
        if pressed:
            self.last_btn2_press = time.time()
        return pressed
    
    def is_gas_detected(self):
        """Check if gas is detected
        Returns: True if gas detected, False if safe
        """
        # Gas sensor is active low (0 when gas detected)
        return not self.gas_sensor.value()
    
    def read_sound_level(self):
        """Read sound level from microphone
        Returns: Sound level (0-4095)
        """
        return self.sound_sensor.read()
    
    def get_sound_voltage(self):
        """Get sound level as voltage
        Returns: Voltage (0-3.3V)
        """
        return self.sound_sensor.read() / 4095.0 * 3.3
    
    def time_since_last_motion(self):
        """Get time since last motion detection
        Returns: Time in seconds
        """
        if self.last_motion_time == 0:
            return 0
        return time.time() - self.last_motion_time
    
    def time_since_button1_press(self):
        """Get time since button 1 was last pressed
        Returns: Time in seconds
        """
        if self.last_btn1_press == 0:
            return 0
        return time.time() - self.last_btn1_press
    
    def time_since_button2_press(self):
        """Get time since button 2 was last pressed
        Returns: Time in seconds
        """
        if self.last_btn2_press == 0:
            return 0
        return time.time() - self.last_btn2_press