from machine import Pin, PWM
import neopixel
import time

# Pin definitions
PIN_LED = 12        # LED output
PIN_BUZZER = 25     # Buzzer PWM
PIN_SERVO = 13      # Servo motor PWM (door)
PIN_WINDOW = 5    # Window servo PWM (new pin for window)
PIN_NEOPIXEL = 26   # Neopixel RGB LEDs
PIN_MOTOR_A = 19    # Motor driver input A
PIN_MOTOR_B = 18    # Motor driver input B
PIN_FAN = 15        # Fan control PWM pin

# Constants
SERVO_FREQ = 50     # Standard servo frequency (50Hz)
SERVO_0_DUTY = 25   # Duty cycle for 0° position
SERVO_90_DUTY = 77  # Duty cycle for 90° position
SERVO_180_DUTY = 128 # Duty cycle for 180° position

# Window servo constants
WINDOW_CLOSED_DUTY = 25    # Duty cycle for closed window
WINDOW_OPEN_DUTY = 128     # Duty cycle for fully open window

NUM_PIXELS = 4      # Number of RGB LEDs in neopixel strip

class ActuatorManager:
    def __init__(self):
        # Initialize all actuators
        self.led = Pin(PIN_LED, Pin.OUT)
        self.buzzer = PWM(Pin(PIN_BUZZER))
        self.buzzer.duty(0)  # Start with buzzer off
        
        # Door servo
        self.servo = PWM(Pin(PIN_SERVO))
        self.servo.freq(SERVO_FREQ)
        
        # Window servo
        try:
            self.window_servo = PWM(Pin(PIN_WINDOW))
            self.window_servo.freq(SERVO_FREQ)
            self.window_servo.duty(WINDOW_CLOSED_DUTY)  # Start with window closed
            self.window_available = True
        except Exception as e:
            print(f"Warning: Could not initialize window servo: {e}")
            self.window_available = False
        
        self.neopixel = neopixel.NeoPixel(Pin(PIN_NEOPIXEL), NUM_PIXELS)
        
        self.motor_a = PWM(Pin(PIN_MOTOR_A, Pin.OUT), 10000)  # 10kHz frequency
        self.motor_b = PWM(Pin(PIN_MOTOR_B, Pin.OUT), 10000)
        self.motor_a.duty(0)  # Start with motor stopped
        self.motor_b.duty(0)
        
        # Initialize fan if available
        try:
            self.fan = PWM(Pin(PIN_FAN, Pin.OUT), 25000)  # 25kHz frequency for fan
            self.fan.duty(0)  # Start with fan off
            self.fan_available = True
        except Exception as e:
            print(f"Warning: Could not initialize fan: {e}")
            self.fan_available = False
        
        print("Actuator manager initialized")
    
    # LED methods
    def led_on(self):
        """Turn on the LED"""
        self.led.value(1)
    
    def led_off(self):
        """Turn off the LED"""
        self.led.value(0)
    
    def led_toggle(self):
        """Toggle the LED state"""
        self.led.value(not self.led.value())
    
    # Buzzer methods
    def buzzer_on(self, freq=1000):
        """Turn on buzzer at specified frequency
        Args:
            freq: Frequency in Hz (default: 1000Hz)
        """
        self.buzzer.freq(freq)
        self.buzzer.duty(512)  # 50% duty cycle
    
    def buzzer_off(self):
        """Turn off buzzer"""
        self.buzzer.duty(0)
    
    def buzzer_beep(self, freq=880, duration=0.2):
        """Make the buzzer beep once
        Args:
            freq: Frequency in Hz (default: 880Hz)
            duration: Beep duration in seconds (default: 0.2s)
        """
        self.buzzer_on(freq)
        time.sleep(duration)
        self.buzzer_off()
    
    # Servo methods for door
    def servo_angle(self, angle):
        """Set door servo to a specific angle
        Args:
            angle: Angle in degrees (0-180)
        """
        # Map angle to duty cycle
        if angle <= 0:
            self.servo.duty(SERVO_0_DUTY)
        elif angle >= 180:
            self.servo.duty(SERVO_180_DUTY)
        else:
            # Linear interpolation
            duty = SERVO_0_DUTY + (angle / 180) * (SERVO_180_DUTY - SERVO_0_DUTY)
            self.servo.duty(int(duty))
    
    def servo_0_degrees(self):
        """Move door servo to 0 degrees position (closed)"""
        self.servo.duty(SERVO_0_DUTY)
    
    def servo_90_degrees(self):
        """Move door servo to 90 degrees position (half open)"""
        self.servo.duty(SERVO_90_DUTY)
    
    def servo_180_degrees(self):
        """Move door servo to 180 degrees position (fully open)"""
        self.servo.duty(SERVO_180_DUTY)
    
    # Window control methods
    def window_open(self, percent=100):
        """Open the window to specified percentage
        
        Args:
            percent: Opening percentage (0-100%)
        """
        if not self.window_available:
            print("Window servo not available")
            return False
            
        # Ensure percent is in valid range
        percent = max(0, min(100, percent))
        
        # Calculate duty cycle based on percentage
        duty = WINDOW_CLOSED_DUTY + (percent / 100) * (WINDOW_OPEN_DUTY - WINDOW_CLOSED_DUTY)
        
        # Set the servo
        self.window_servo.duty(int(duty))
        print(f"Window opened to {percent}%")
        return True
    
    def window_close(self):
        """Close the window completely"""
        if not self.window_available:
            print("Window servo not available")
            return False
            
        self.window_servo.duty(WINDOW_CLOSED_DUTY)
        print("Window closed")
        return True
    
    def window_ventilate(self):
        """Open the window partially for ventilation (30%)"""
        return self.window_open(30)
    
    def window_control_by_temperature(self, temperature, humidity=None):
        """Control window opening based on temperature and humidity
        
        Args:
            temperature: Current temperature in °C
            humidity: Current humidity % (optional)
            
        Returns:
            int: Window opening percentage
        """
        if not self.window_available:
            print("Window servo not available")
            return 0
        
        # Simple temperature-based algorithm
        if temperature > 28:
            # Hot - open wide
            percent = 100
        elif temperature > 25:
            # Warm - open partially
            percent = 50
        elif temperature > 22:
            # Slightly warm - vent
            percent = 20
        else:
            # Cool or cold - close
            percent = 0
        
        # If humidity is too high, open for ventilation regardless
        if humidity and humidity > 75 and percent < 20:
            percent = 20
        
        self.window_open(percent)
        return percent
    
    # Neopixel RGB LED methods
    def rgb_set_all(self, r, g, b, brightness=100):
        """Set all RGB LEDs to the same color
        Args:
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)
            brightness: Brightness scaling (0-100%)
        """
        # Scale by brightness
        r = int(r * brightness / 100)
        g = int(g * brightness / 100)
        b = int(b * brightness / 100)
        
        # Set all pixels
        for i in range(NUM_PIXELS):
            self.neopixel[i] = (r, g, b)
        self.neopixel.write()
    
    # Motor methods
    def motor_forward(self, speed=600):
        """Run motor forward
        Args:
            speed: Motor speed (0-1023)
        """
        self.motor_a.duty(speed)
        self.motor_b.duty(0)
    
    def motor_backward(self, speed=600):
        """Run motor backward
        Args:
            speed: Motor speed (0-1023)
        """
        self.motor_a.duty(0)
        self.motor_b.duty(speed)
    
    def motor_stop(self):
        """Stop the motor"""
        self.motor_a.duty(0)
        self.motor_b.duty(0)
    
    # Fan methods
    def fan_set_speed(self, speed_percent):
        """Set fan speed as percentage
        Args:
            speed_percent: Fan speed (0-100%)
        """
        if not hasattr(self, 'fan') or not self.fan_available:
            print("Fan not available")
            return False
            
        # Ensure speed is within valid range
        speed_percent = max(0, min(100, speed_percent))
        
        # Convert percentage to duty cycle (0-1023)
        duty = int(speed_percent * 10.23)
        self.fan.duty(duty)
        print(f"Fan speed set to {speed_percent}%")
        return True