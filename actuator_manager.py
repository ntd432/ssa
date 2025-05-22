from machine import Pin, PWM
import neopixel
import time

# Pin definitions
PIN_LED = 12        # LED output
PIN_BUZZER = 25     # Buzzer PWM
PIN_SERVO = 13      # Servo motor PWM
PIN_NEOPIXEL = 26   # Neopixel RGB LEDs
PIN_MOTOR_A = 19    # Motor driver input A
PIN_MOTOR_B = 18    # Motor driver input B
PIN_WINDOW = 5      # Window servo PWM pin (uses pin 5 as in your example)

# Constants
SERVO_FREQ = 50     # Standard servo frequency (50Hz)
SERVO_FREQ_OFF = 0
SERVO_0_DUTY = 25   # Duty cycle for 0° position
SERVO_90_DUTY = 77  # Duty cycle for 90° position
SERVO_180_DUTY = 128 # Duty cycle for 180° position

NUM_PIXELS = 4      # Number of RGB LEDs in neopixel strip

# Window servo constants
WINDOW_FREQ_OFF = 0    # Standard servo frequency (50Hz)
WINDOW_FREQ = 50
WINDOW_CLOSED_DUTY = 100  # Duty cycle for closed window (from your example)
WINDOW_OPEN_DUTY = 46     # Duty cycle for open window (from your example)

class ActuatorManager:
    def __init__(self):
        # Initialize all actuators
        self.led = Pin(PIN_LED, Pin.OUT)
        self.buzzer = PWM(Pin(PIN_BUZZER))
        self.buzzer.duty(0)  # Start with buzzer off
        
        self.servo = PWM(Pin(PIN_SERVO))
        self.servo.freq(SERVO_FREQ_OFF)
        
        self.neopixel = neopixel.NeoPixel(Pin(PIN_NEOPIXEL), NUM_PIXELS)
        
        self.motor_a = PWM(Pin(PIN_MOTOR_A, Pin.OUT), 10000)  # 10kHz frequency
        self.motor_b = PWM(Pin(PIN_MOTOR_B, Pin.OUT), 10000)
        self.motor_a.duty(0)  # Start with motor stopped
        self.motor_b.duty(0)
        
        # Initialize window servo
        self.window_servo = PWM(Pin(PIN_WINDOW))
        self.window_servo.freq(WINDOW_FREQ_OFF)
        self.window_servo.duty(WINDOW_CLOSED_DUTY)  # Start with window closed
        
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
    
    def play_happy_birthday(self):
        """Play Happy Birthday tune on buzzer"""
        notes = [294, 440, 392, 532, 494, 392, 440, 392, 587, 532, 
                 392, 784, 659, 532, 494, 440, 698, 659, 532, 587, 532]
        for note in notes:
            self.buzzer.freq(note)
            self.buzzer.duty(1000)
            time.sleep(0.25)
        self.buzzer.duty(0)
    
    # Servo methods
    def servo_angle(self, angle):
        """Set servo to a specific angle
        Args:
            angle: Angle in degrees (0-180)
        """
        self.servo.freq(SERVO_FREQ)

        # Map angle to duty cycle
        if angle <= 0:
            self.servo.duty(SERVO_0_DUTY)
        elif angle >= 180:
            self.servo.duty(SERVO_180_DUTY)
        else:
            # Linear interpolation
            duty = SERVO_0_DUTY + (angle / 180) * (SERVO_180_DUTY - SERVO_0_DUTY)
            self.servo.duty(int(duty))
        self.servo.freq(SERVO_FREQ_OFF)

    def servo_0_degrees(self):
        """Move servo to 0 degrees position"""
        self.servo_angle(0)
    
    def servo_90_degrees(self):
        """Move servo to 90 degrees position"""
        self.servo_angle(90)
    
    def servo_180_degrees(self):
        """Move servo to 180 degrees position"""
        self.servo_angle(180)
    
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
    
    def rgb_set_pixel(self, index, r, g, b, brightness=100):
        """Set a specific RGB LED to a color
        Args:
            index: LED index (0-3)
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)
            brightness: Brightness scaling (0-100%)
        """
        if 0 <= index < NUM_PIXELS:
            # Scale by brightness
            r = int(r * brightness / 100)
            g = int(g * brightness / 100)
            b = int(b * brightness / 100)
            
            self.neopixel[index] = (r, g, b)
            self.neopixel.write()
    
    def rgb_off(self):
        """Turn off all RGB LEDs"""
        self.rgb_set_all(0, 0, 0)
    
    def rgb_red(self, brightness=100):
        """Set all LEDs to red"""
        self.rgb_set_all(255, 0, 0, brightness)
    
    def rgb_green(self, brightness=100):
        """Set all LEDs to green"""
        self.rgb_set_all(0, 255, 0, brightness)
    
    def rgb_blue(self, brightness=100):
        """Set all LEDs to blue"""
        self.rgb_set_all(0, 0, 255, brightness)
    
    def rgb_white(self, brightness=100):
        """Set all LEDs to white"""
        self.rgb_set_all(255, 255, 255, brightness)
    
    # Motor methods
    def motor_forward(self, speed=600):
        """Run motor forward
        Args:
            speed: Motor speed (0-1023)
        """
        self.motor_a.duty(speed)
        self.motor_b.duty(1)
    
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
    
    # Window methods
    def window_open(self):
        """Open the window"""
        self.window_servo.freq(WINDOW_FREQ)
        self.window_servo.duty(WINDOW_OPEN_DUTY)
        time.sleep(1)
        self.window_servo.freq(WINDOW_FREQ_OFF)

    
    def window_close(self):
        """Close the window"""
        self.window_servo.freq(WINDOW_FREQ)
        self.window_servo.duty(WINDOW_CLOSED_DUTY)
        time.sleep(1)
        self.window_servo.freq(WINDOW_FREQ_OFF)
    
    def window_toggle(self):
        """Toggle the window state"""
        current_duty = self.window_servo.duty()
        if current_duty == WINDOW_CLOSED_DUTY:
            self.window_servo.duty(WINDOW_OPEN_DUTY)
        else:
            self.window_servo.duty(WINDOW_CLOSED_DUTY)