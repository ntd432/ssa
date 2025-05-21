from machine import Pin, PWM
import time
import neopixel

# Pin definitions
COFFEE_BUTTON = 16  # Button 1 (left button) with pull-up
BUZZER_PIN = 25     # Buzzer for coffee sounds
LED_PIN = 26        # Neopixel RGB LEDs

# Coffee time settings
COFFEE_CUTOFF_HOUR = 17  # 5 PM - no coffee after this time

# Create a class for the coffee habit tracker
class CoffeeHabitTracker:
    def __init__(self):
        """Initialize the coffee habit tracker components"""
        # Set up button with pull-up resistor (active low)
        self.coffee_button = Pin(COFFEE_BUTTON, Pin.IN, Pin.PULL_UP)
        
        # Set up buzzer for coffee sounds
        self.buzzer = PWM(Pin(BUZZER_PIN))
        self.buzzer.duty(0)  # Start with buzzer off
        
        # Set up RGB LEDs for visual feedback
        self.rgb_leds = neopixel.NeoPixel(Pin(LED_PIN), 4)
        
        # Status tracking
        self.brewing = False
        self.coffee_count = 0
        
        print("Coffee Habit Tracker initialized")
    
    def check_time_allowed(self):
        """Check if coffee is allowed at the current time
        
        Returns:
            bool: True if coffee is allowed, False if too late
        """
        current_time = time.localtime()
        current_hour = current_time[3]  # Hour in 24h format
        
        # No coffee after cutoff time (5 PM)
        return current_hour < COFFEE_CUTOFF_HOUR
    
    def brew_coffee(self):
        """Simulate coffee brewing with lights and sounds"""
        self.brewing = True
        self.coffee_count += 1
        
        print("Brewing coffee...")
        
        # Set all LEDs to coffee brown color
        self.set_coffee_color()
        
        # Brewing phases with sounds
        # Phase 1: Initial water heating
        self.buzzer.freq(220)  # Low hum for heating
        self.buzzer.duty(300)  # Lower volume
        time.sleep(1)
        
        # Phase 2: Initial brewing/dripping
        for _ in range(5):
            self.buzzer.freq(900)  # High pitch for water
            self.buzzer.duty(200)
            time.sleep(0.1)
            self.buzzer.duty(0)
            time.sleep(0.2)
        
        # Phase 3: Main brewing phase
        self.buzzer.freq(350)  # Medium pitch for steady brewing
        self.buzzer.duty(400)
        time.sleep(1.5)
        
        # Phase 4: Final drips
        for _ in range(3):
            self.buzzer.freq(800)
            self.buzzer.duty(200)
            time.sleep(0.1)
            self.buzzer.duty(0)
            time.sleep(0.3)
        
        # Coffee ready!
        self.buzzer.duty(0)  # Stop sound
        
        # Pulse the LEDs to indicate coffee is ready
        for brightness in range(100, 0, -10):
            self.set_coffee_color(brightness)
            time.sleep(0.05)
        
        for brightness in range(0, 101, 10):
            self.set_coffee_color(brightness)
            time.sleep(0.05)
            
        time.sleep(1)
        
        # Turn off LEDs
        self.turn_off_leds()
        self.brewing = False
        print("Coffee ready! Enjoy!")
    
    def deny_coffee(self):
        """Display feedback when coffee is denied due to late hour"""
        print("Coffee denied: It's too late for coffee!")
        
        # Visual indicator - red LEDs
        self.set_all_leds(255, 0, 0)  # Red
        
        # Sound warning
        for _ in range(2):
            self.buzzer.freq(200)  # Low warning tone
            self.buzzer.duty(512)
            time.sleep(0.2)
            self.buzzer.duty(0)
            time.sleep(0.1)
        
        time.sleep(1)
        
        # Turn off LEDs
        self.turn_off_leds()
    
    def set_coffee_color(self, brightness=100):
        """Set all LEDs to coffee brown color
        
        Args:
            brightness: Brightness level (0-100%)
        """
        # Coffee brown color (RGB: 76, 46, 0)
        r = int(76 * brightness / 100)
        g = int(46 * brightness / 100)
        b = int(0 * brightness / 100)
        
        self.set_all_leds(r, g, b)
    
    def set_all_leds(self, r, g, b):
        """Set all LEDs to the same color
        
        Args:
            r: Red component (0-255)
            g: Green component (0-255)
            b: Blue component (0-255)
        """
        for i in range(4):
            self.rgb_leds[i] = (r, g, b)
        self.rgb_leds.write()
    
    def turn_off_leds(self):
        """Turn off all LEDs"""
        self.set_all_leds(0, 0, 0)
    
    def run(self):
        """Main loop for the coffee habit tracker"""
        print("Coffee Habit Tracker running!")
        print("Press the left button to brew coffee")
        
        try:
            # Display initial color to show system is ready
            self.set_all_leds(0, 0, 50)  # Soft blue
            time.sleep(1)
            self.turn_off_leds()
            
            while True:
                # Check if coffee button is pressed (active low)
                if not self.coffee_button.value() and not self.brewing:
                    # Wait for button release to avoid multiple triggers
                    while not self.coffee_button.value():
                        time.sleep(0.01)
                    
                    # Check if coffee is allowed at this hour
                    if self.check_time_allowed():
                        self.brew_coffee()
                    else:
                        self.deny_coffee()
                        
                        # Display the time and message on LCD if available
                        current_time = time.localtime()
                        hour = current_time[3]
                        minute = current_time[4]
                        time_str = f"{hour:02d}:{minute:02d}"
                        print(f"Current time: {time_str}")
                        print("No coffee after 5 PM for better sleep")
                
                # Small delay to prevent tight loop
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            # Clean up
            self.turn_off_leds()
            self.buzzer.duty(0)
            print("Coffee Habit Tracker stopped")

# Run the coffee habit tracker if this script is executed directly
if __name__ == "__main__":
    coffee_tracker = CoffeeHabitTracker()
    coffee_tracker.run()