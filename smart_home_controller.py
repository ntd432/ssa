from sensor_manager import SensorManager
from actuator_manager import ActuatorManager
from display_manager import DisplayManager
from web_manager import WebManager
from rfid_manager import RFIDManager  # Import the new RFID manager
from light_control import LightManager
import time

class SmartHomeController:
    def __init__(self):
        print("Initializing Smart Home Controller...")
        
        # Initialize all component managers
        self.sensors = SensorManager()
        self.actuators = ActuatorManager()
        self.display = DisplayManager()
        self.web = WebManager()
        self.rfid = RFIDManager()
        self.light = LightManager()  # Add the light manager
        
        # Display welcome message
        #self.display.display_two_lines("Smart Home", "System Ready")
        #time.sleep(2)
        
        # Add some test authorized cards (replace with real card IDs)
        #self.rfid.add_authorized_card("12345678", "Admin Card")
        #self.rfid.add_authorized_card("87654321", "Guest Card")
        
        print("Smart Home Controller initialized")
    
    def connect_to_wifi(self, ssid=None, password=None):
        """Connect to WiFi network
        Args:
            ssid: Network name (optional)
            password: Network password (optional)
        """
        if ssid and password:
            self.web.ssid = ssid
            self.web.password = password
        
        self.display.display_two_lines("Connecting to", self.web.ssid)
        if self.web.connect():
            self.actuators.rgb_green()
            self.display.display_two_lines("WiFi Connected", "IP: " + self.web.wlan.ifconfig()[0])
            time.sleep(2)
            self.actuators.rgb_off()
        else:
            self.actuators.rgb_red()
            self.display.display_two_lines("WiFi Failed", "Check settings")
            time.sleep(2)
            self.actuators.rgb_off()
    
    def motion_detection_demo(self):
        """Demo function for motion detection with PIR sensor"""
        print("Starting motion detection demo")
        self.display.display_two_lines("Motion Detection", "Demo Running")
        
        try:
            while True:
                if self.sensors.is_motion_detected():
                    self.actuators.led_on()
                    self.actuators.rgb_red()
                    self.display.display_two_lines("Motion Detected!", "")
                else:
                    self.actuators.led_off()
                    self.actuators.rgb_off()
                    self.display.display_two_lines("No Motion", "")
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.actuators.led_off()
            self.actuators.rgb_off()
            print("Motion detection demo stopped")
    
    def temperature_monitor_demo(self):
        """Demo function for temperature and humidity monitoring"""
        print("Starting temperature monitor demo")
        self.display.display_two_lines("Temp & Humidity", "Demo Running")
        
        try:
            while True:
                temp, humidity = self.sensors.read_temperature_humidity()
                
                # Display values on LCD
                self.display.display_sensor_values(temp, humidity)
                
                # Visual feedback based on temperature
                if temp > 28:
                    self.actuators.rgb_red()  # Hot - red
                elif temp < 20:
                    self.actuators.rgb_blue()  # Cold - blue
                else:
                    self.actuators.rgb_green()  # Comfortable - green
                
                # Send data to server every 30 seconds
                if int(time.time()) % 30 == 0:
                    data = {
                        "timestamp": time.time(),
                        "temperature": temp,
                        "humidity": humidity
                    }
                    self.web.send_data(data, "temperature")
                
                time.sleep(1)
        except KeyboardInterrupt:
            self.actuators.rgb_off()
            print("Temperature monitor demo stopped")
    
    def rfid_access_control_demo(self):
        """Demo function for RFID card access control"""
        print("Starting RFID access control demo")
        self.display.display_two_lines("RFID Access", "Scan your card")
        
        # Set up some environmental variables for the demo
        door_open = False
        door_lock_timeout = 0
        auto_lock_time = 5  # Auto-lock door after 5 seconds
        
        try:
            while True:
                # Check if a card is present
                if self.rfid.check_card():
                    card_id = self.rfid.get_card_id()
                    self.display.display_two_lines("Card Detected", card_id[:16])
                    
                    # Check if this is an authorized card
                    if self.rfid.is_card_authorized():
                        name = self.rfid.get_authorized_card_name()
                        self.display.display_two_lines("Access Granted", name)
                        
                        # Visual and audio feedback
                        self.actuators.rgb_green()
                        self.actuators.buzzer_beep(880, 0.1)
                        
                        # Open the door
                        self.actuators.servo_angle(180)
                        door_open = True
                        door_lock_timeout = time.time() + auto_lock_time
                        
                        print(f"Door opened for {name}")
                        
                        # Wait a moment to prevent multiple scans
                        time.sleep(0.5)
                    else:
                        self.display.display_two_lines("Access Denied", "Unknown Card")
                        
                        # Visual and audio feedback for denied access
                        self.actuators.rgb_red()
                        for _ in range(2):  # Two quick error beeps
                            self.actuators.buzzer_beep(220, 0.2)
                            time.sleep(0.1)
                        
                        print(f"Access denied for card: {card_id}")
                        time.sleep(1)
                        self.actuators.rgb_off()
                
                # Auto-lock the door after timeout
                if door_open and time.time() > door_lock_timeout:
                    self.display.display_two_lines("Auto-locking", "Door secured")
                    self.actuators.servo_angle(0)  # Close door/gate
                    self.actuators.buzzer_beep(440, 0.1)  # Confirmation beep
                    door_open = False
                    self.actuators.rgb_off()
                    time.sleep(1)
                    self.display.display_two_lines("RFID Access", "Scan your card")
                
                # Manual lock with button 1 (if door is open)
                if door_open and self.sensors.is_button1_pressed():
                    self.display.display_two_lines("Manual Lock", "Door secured")
                    self.actuators.servo_angle(0)  # Close door/gate
                    self.actuators.buzzer_beep(440, 0.1)  # Confirmation beep
                    door_open = False
                    self.actuators.rgb_off()
                    
                    # Wait for button release
                    while self.sensors.is_button1_pressed():
                        time.sleep(0.01)
                    
                    time.sleep(1)
                    self.display.display_two_lines("RFID Access", "Scan your card")
                
                # Button 2 can add a temporary access card
                if self.sensors.is_button2_pressed():
                    self.display.display_two_lines("Add New Card", "Scan card now")
                    self.actuators.rgb_blue()
                    
                    # Wait for button release
                    while self.sensors.is_button2_pressed():
                        time.sleep(0.01)
                    
                    # Wait for a new card (with 10 second timeout)
                    new_card = self.rfid.wait_for_card(timeout=10)
                    
                    if new_card:
                        # Add this card with temporary access
                        self.rfid.add_authorized_card(new_card, "Temp Guest")
                        self.display.display_two_lines("Card Added", new_card[:16])
                        self.actuators.rgb_green()
                        self.actuators.buzzer_beep(880, 0.1)
                        print(f"Added temporary access card: {new_card}")
                    else:
                        # No card presented in time
                        self.display.display_two_lines("Timeout", "No card scanned")
                        self.actuators.rgb_red()
                        self.actuators.buzzer_beep(220, 0.3)
                    
                    time.sleep(2)
                    self.actuators.rgb_off()
                    self.display.display_two_lines("RFID Access", "Scan your card")
                
                # Standby state - slight delay to prevent tight loop
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            # Clean up on exit
            self.actuators.servo_angle(0)  # Ensure door is closed
            self.actuators.rgb_off()
            self.actuators.buzzer_off()
            print("RFID access control demo stopped")
    
    def gas_detector_demo(self):
        """Demo function for gas detection"""
        print("Starting gas detector demo")
        self.display.display_two_lines("Gas Detector", "Demo Running")
        
        try:
            while True:
                if self.sensors.is_gas_detected():
                    self.actuators.led_on()
                    self.actuators.buzzer_beep(880, 0.1)
                    self.actuators.rgb_green()
                    self.display.display_two_lines("GAS DETECTED!", "DANGER")
                else:
                    self.actuators.led_off()
                    self.actuators.rgb_green()
                    self.display.display_two_lines("Air Quality", "Normal")
                time.sleep(0.2)
        except KeyboardInterrupt:
            self.actuators.led_off()
            self.actuators.buzzer_off()
            self.actuators.rgb_off()
            print("Gas detector demo stopped")
    
    def servo_test_demo(self):
        """Demo function for servo motor control"""
        print("Starting servo test demo")
        self.display.display_two_lines("Servo Test", "Demo Running")
        
        try:
            while True:
                # Sweep from 0 to 180 degrees
                for angle in range(0, 181, 10):
                    self.actuators.servo_angle(angle)
                    self.display.display_two_lines("Servo Test", f"Angle: {angle}")
                    time.sleep(0.1)
                
                # Sweep from 180 to 0 degrees
                for angle in range(180, -1, -10):
                    self.actuators.servo_angle(angle)
                    self.display.display_two_lines("Servo Test", f"Angle: {angle}")
                    time.sleep(0.1)
        except KeyboardInterrupt:
            self.actuators.servo_angle(90)  # Return to middle position
            print("Servo test demo stopped")
    
    def button_led_control_demo(self):
        """Demo function for button control of LED"""
        print("Starting button LED control demo")
        self.display.display_two_lines("Button Control", "Press to toggle")
        
        led_state = False
        
        try:
            while True:
                # Check if button 1 is pressed
                if self.sensors.is_button1_pressed():
                    led_state = not led_state
                    if led_state:
                        self.actuators.led_on()
                        self.display.display_two_lines("LED Control", "LED: ON")
                    else:
                        self.actuators.led_off()
                        self.display.display_two_lines("LED Control", "LED: OFF")
                    # Wait for button release
                    while self.sensors.is_button1_pressed():
                        time.sleep(0.01)
                
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.actuators.led_off()
            print("Button LED control demo stopped")
    
    def run_security_system(self):
        """Run a complete security system with RFID, motion detection, and gas sensors"""
        print("Starting security system")
        self.display.display_two_lines("Security System", "Running")
        
        # Security system states
        armed = False
        alarm_triggered = False
        
        try:
            while True:
                # Check for RFID card scan
                if self.rfid.check_card():
                    card_id = self.rfid.get_card_id()
                    
                    # Check if this is an authorized card
                    if self.rfid.is_card_authorized():
                        name = self.rfid.get_authorized_card_name()
                        armed = not armed  # Toggle armed state
                        
                        if armed:
                            self.actuators.rgb_green()
                            self.actuators.buzzer_beep(880, 0.2)
                            self.display.display_two_lines("System Armed", name)
                        else:
                            self.actuators.rgb_blue()
                            self.actuators.buzzer_beep(440, 0.1)
                            self.display.display_two_lines("System Disarmed", name)
                            alarm_triggered = False  # Reset alarm state when disarmed
                        
                        time.sleep(2)
                    else:
                        self.actuators.rgb_red()
                        self.actuators.buzzer_beep(220, 0.5)
                        self.display.display_two_lines("Access Denied", "Unknown Card")
                        time.sleep(1)
                
                # If armed, check sensors for security events
                if armed:
                    if not alarm_triggered:  # Only show "System Armed" when not in alarm state
                        self.actuators.rgb_green()
                        self.display.display_two_lines("System Armed", "Monitoring...")
                    
                    # Check for motion
                    if self.sensors.is_motion_detected():
                        alarm_triggered = True
                        self.actuators.rgb_red()
                        self.display.display_two_lines("MOTION DETECTED!", "Alarm Triggered")
                        self.actuators.buzzer_on(880)  # Alarm sound
                    
                    # Check for gas
                    if self.sensors.is_gas_detected():
                        alarm_triggered = True
                        self.actuators.rgb_red()
                        self.display.display_two_lines("GAS DETECTED!", "Alarm Triggered")
                        self.actuators.buzzer_on(440)  # Different alarm sound
                else:
                    # System is disarmed
                    self.actuators.rgb_off()
                
                # Button override to stop alarm
                if alarm_triggered and self.sensors.is_button1_pressed():
                    alarm_triggered = False
                    self.actuators.buzzer_off()
                    self.display.display_two_lines("Alarm Silenced", "System still armed")
                    self.actuators.rgb_green()
                    # Wait for button release
                    while self.sensors.is_button1_pressed():
                        time.sleep(0.01)
                
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.actuators.rgb_off()
            self.actuators.buzzer_off()
            print("Security system stopped")
    
    def light_test_demo(self):
        """Demo function for light control testing"""
        print("Starting light test demo")
        self.display.display_two_lines("Light Control", "Testing...")
        
        self.light._test_cycle()
        
        print("Light test demo finished")
    
    def auto_light_demo(self):
        """Demo function for automatic light control based on time"""
        print("Starting automatic light control demo")
        self.display.display_two_lines("Auto Light", "Demo Running")
        
        try:
            while True:
                current_time = self.light.get_current_time_seconds()
                hours = current_time // 3600
                minutes = (current_time % 3600) // 60
                
                brightness = self.light.adjust_brightness_for_time()
                
                self.display.display_two_lines(
                    f"Time: {hours:02d}:{minutes:02d}",
                    f"Bright: {brightness:.0f}%"
                )
                
                time.sleep(10)  # Update every 10 seconds
                
        except KeyboardInterrupt:
            self.light.lights_off()
            print("Auto light demo stopped")
    
    def sunrise_demo(self):
        """Demo function for sunrise simulation"""
        print("Starting sunrise simulation demo")
        self.display.display_two_lines("Sunrise", "Simulation")
        
        # Use a shorter duration for demo purposes
        self.light.simulate_sunrise(duration_minutes=1)
        
        self.display.display_two_lines("Sunrise", "Complete")
        time.sleep(2)

    def coffee_tracker_demo(self):
        """Demo function for the coffee habit tracker"""
        from coffee_habit_tracker import CoffeeHabitTracker
        
        print("Starting Coffee Habit Tracker")
        self.display.display_two_lines("Coffee Tracker", "Press left button")
        
        # Create coffee tracker
        coffee = CoffeeHabitTracker()
        
        try:
            # Initial display
            self.actuators.rgb_blue(20)  # Dim blue to show system is ready
            time.sleep(1)
            self.actuators.rgb_off()
            
            while True:
                # Check if coffee button is pressed (active low)
                if self.sensors.is_button1_pressed() and not coffee.brewing:
                    # Check if coffee is allowed at this hour
                    if coffee.check_time_allowed():
                        # Update display
                        self.display.display_two_lines("Brewing Coffee", "Please wait...")
                        
                        # Brew coffee with visual and sound effects
                        coffee.brew_coffee()
                        
                        # Update display with count
                        self.display.display_two_lines("Coffee Ready!", f"Count today: {coffee.coffee_count}")
                        time.sleep(2)
                        self.display.display_two_lines("Coffee Tracker", "Press left button")
                    else:
                        # Coffee denied due to late hour
                        current_time = time.localtime()
                        hour = current_time[3]
                        minute = current_time[4]
                        time_str = f"{hour:02d}:{minute:02d}"
                        
                        self.display.display_two_lines("Too Late!", f"Time: {time_str}")
                        coffee.deny_coffee()
                        
                        # More detailed message
                        self.display.display_two_lines("No coffee after", "5 PM for sleep")
                        time.sleep(2)
                        self.display.display_two_lines("Coffee Tracker", "Press left button")
                
                # Small delay to prevent tight loop
                time.sleep(0.1)
                    
        except KeyboardInterrupt:
            # Clean up
            coffee.turn_off_leds()
            coffee.buzzer.duty(0)
            self.actuators.rgb_off()
            print("Coffee tracker demo stopped")
    
    def door_test_continuous(self):
        """Test the door servo continuously by moving it through its full range
        with 1 second pauses between movements."""
        
        print("Starting continuous door test")
        self.display.display_two_lines("Door Test", "Running...")
        
        try:
            count = 0
            while True:
                # Open the door (180 degrees)
                self.display.display_two_lines("Door Test", "Opening door")
                self.actuators.servo_angle(180)
                print(f"Door opened ({count})")
                time.sleep(1)
                
                # Close the door (0 degrees)
                self.display.display_two_lines("Door Test", "Closing door")
                self.actuators.servo_angle(0)
                print(f"Door closed ({count})")
                time.sleep(1)
                
                # Middle position (90 degrees)
                self.display.display_two_lines("Door Test", "Middle position")
                self.actuators.servo_angle(90)
                print(f"Door middle ({count})")
                time.sleep(1)
                
                count += 1
                
        except KeyboardInterrupt:
            # Return to closed position when stopping
            self.actuators.servo_angle(0)
            self.display.display_two_lines("Door Test", "Stopped")
            print("Door test stopped")
    
    def window_test_demo(self):
        """Test the window servo by moving it through various positions"""
        
        print("Starting window test demo")
        self.display.display_two_lines("Window Test", "Running...")
        
        try:
            # Close window (0%)
            self.display.display_two_lines("Window Test", "Closing window")
            self.actuators.window_close()
            print("Window closed")
            time.sleep(2)
            
            # Open window partially (30%)
            self.display.display_two_lines("Window Test", "Ventilation 30%")
            self.actuators.window_open(30)
            print("Window at 30%")
            time.sleep(2)
            
            # Open window halfway (50%)
            self.display.display_two_lines("Window Test", "Opening 50%")
            self.actuators.window_open(50)
            print("Window at 50%")
            time.sleep(2)
            
            # Open window fully (100%)
            self.display.display_two_lines("Window Test", "Opening 100%")
            self.actuators.window_open(100)
            print("Window fully open")
            time.sleep(2)
            
            # Test temperature-based control
            self.display.display_two_lines("Window Test", "Temp control")
            
            # Simulate different temperatures
            temp_scenarios = [
                (18, "Cold - Closed"),
                (23, "Mild - Venting"),
                (26, "Warm - Half Open"),
                (30, "Hot - Fully Open")
            ]
            
            for temp, desc in temp_scenarios:
                percentage = self.actuators.window_control_by_temperature(temp)
                self.display.display_two_lines(f"{desc}", f"Temp: {temp}°C ({percentage}%)")
                time.sleep(2)
            
            # Close window at the end
            self.display.display_two_lines("Window Test", "Test Complete")
            self.actuators.window_close()
            time.sleep(1)
            
        except KeyboardInterrupt:
            # Return window to closed position when stopping
            self.actuators.window_close()
            self.display.display_two_lines("Window Test", "Stopped")
            print("Window test stopped")
    
    def climate_control_demo(self):
        """Demonstrate automatic climate control using temperature and window/fan"""
        
        print("Starting climate control demo")
        self.display.display_two_lines("Climate Control", "Demo Running")
        
        try:
            while True:
                # Read current temperature and humidity
                temp, humidity = self.sensors.read_temperature_humidity()
                
                # Set window position based on temperature
                window_percent = self.actuators.window_control_by_temperature(temp, humidity)
                
                # Set fan speed based on temperature
                if hasattr(self.actuators, 'fan_available') and self.actuators.fan_available:
                    fan_speed = self.actuators.fan_auto_mode(temp)
                else:
                    fan_speed = 0
                
                # Update display
                self.display.display_two_lines(
                    f"Temp: {temp:.1f}°C {humidity:.0f}%",
                    f"Win: {window_percent}% Fan: {fan_speed}%"
                )
                
                # Wait before next update
                time.sleep(5)
                
        except KeyboardInterrupt:
            # Clean up
            self.actuators.window_close()
            if hasattr(self.actuators, 'fan_available') and self.actuators.fan_available:
                self.actuators.fan_set_speed(0)
            self.display.display_two_lines("Climate Control", "Demo Stopped")
            print("Climate control demo stopped")

# Example usage
if __name__ == "__main__":
    controller = SmartHomeController()
    
    # Uncomment one of these to run a specific demo
    #controller.connect_to_wifi("Google Pixel 8 Pro", "Matebook17")
    #controller.motion_detection_demo()
    #controller.temperature_monitor_demo()
    #controller.gas_detector_demo()
    #controller.servo_test_demo()
    #controller.button_led_control_demo()
    #controller.rfid_access_control_demo()
    #controller.run_security_system()
    controller.coffee_tracker_demo()
    #controller.door_test_continuous()