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
        self.display.display_two_lines("Smart Home", "System Ready")
        time.sleep(2)
        
        # Add some test authorized cards (replace with real card IDs)
        self.rfid.add_authorized_card("12345678", "Admin Card")
        self.rfid.add_authorized_card("87654321", "Guest Card")
        
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

# Example usage
if __name__ == "__main__":
    controller = SmartHomeController()
    
    # Uncomment one of these to run a specific demo
    #controller.connect_to_wifi("Google Pixel 8 Pro", "Matebook17")
    #controller.motion_detection_demo()
    #controller.temperature_monitor_demo()
    #controller.gas_detector_demo()
    controller.servo_test_demo()
    #controller.button_led_control_demo()
    #controller.rfid_access_control_demo()
    #controller.run_security_system()