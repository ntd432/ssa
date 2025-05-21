from smart_home_controller import SmartHomeController
from coffee_habit_tracker import CoffeeHabitTracker
from light_control import LightManager
from phone_controller import PhoneController
import time

class SmartSleepAssistant:
    """Main logic for Smart Sleep Assistant system"""
    
    def __init__(self, use_simulated_time=False, time_factor=1):
        # Initialize all component controllers
        print("Initializing Smart Sleep Assistant...")
        self.controller = SmartHomeController()
        self.light = LightManager()
        self.phone_controller = PhoneController()
        self.coffee_tracker = CoffeeHabitTracker()
        
        # Time simulation configuration
        self.use_simulated_time = use_simulated_time  # Enable/disable simulated time
        self.time_factor = time_factor                # Time acceleration factor
        self.simulated_hour = 12                      # Default start: noon
        self.simulated_minute = 0
        self.simulated_second = 0
        self.simulation_start_time = time.time()      # Real time when simulation started
        self.last_update_time = self.simulation_start_time
        
        # Set time parameters (in seconds since midnight)
        self.sleep_time = 22 * 3600  # 10 PM
        self.wake_time = 7 * 3600    # 7 AM
        self.pre_sleep_time = self.sleep_time - 3600  # 1 hour before sleep time
        self.pre_wake_time = self.wake_time - 3600    # 1 hour before wake time
        
        # Coffee cutoff time
        self.coffee_cutoff_soft = 17 * 3600  # 5 PM - warning
        self.coffee_cutoff_hard = 18 * 3600  # 6 PM - no coffee allowed
        
        # Sleep environment parameters
        self.optimal_sleep_temp = 17  # Optimal sleeping temperature in °C
        self.max_sleep_humidity = 60  # Maximum acceptable humidity during sleep
        
        # System states
        self.night_mode = False
        self.coffee_warning_active = False
        self.coffee_warning_time = 0
        self.coffee_double_confirm_timeout = 10  # Seconds to confirm coffee after warning
        
        # Initialize display
        if self.use_simulated_time:
            self.controller.display.display_two_lines(
                "SIMULATION MODE", 
                f"Time Factor: {time_factor}x"
            )
            time.sleep(2)
        
        self.controller.display.display_two_lines("Sleep Assistant", "System Ready")
        print("Smart Sleep Assistant initialized")
    
    def set_simulated_time(self, hour, minute=0, second=0):
        """Set the simulated time to a specific hour, minute, second
        
        Args:
            hour: Hour in 24-hour format (0-23)
            minute: Minute (0-59)
            second: Second (0-59)
        """
        # Validate inputs
        hour = max(0, min(23, hour))
        minute = max(0, min(59, minute))
        second = max(0, min(59, second))
        
        self.simulated_hour = hour
        self.simulated_minute = minute
        self.simulated_second = second
        
        # Reset simulation start time
        self.simulation_start_time = time.time()
        self.last_update_time = self.simulation_start_time
        
        # Update the display to show the new time
        sim_time = self.format_time(self.get_current_time_seconds())
        self.controller.display.display_two_lines(
            "Time Set:", 
            f"{sim_time} ({self.time_factor}x)"
        )
        
        print(f"Simulated time set to {sim_time} with {self.time_factor}x acceleration")
        time.sleep(1)
    
    def set_time_factor(self, factor):
        """Set the time acceleration factor
        
        Args:
            factor: Multiplier for time passage (1 = real time, 60 = 1 minute per second)
        """
        if factor < 1:
            factor = 1  # Minimum is real time
        
        self.time_factor = factor
        
        # Reset simulation timing to avoid jumps
        current_seconds = self.get_current_time_seconds()
        self.simulation_start_time = time.time()
        self.last_update_time = self.simulation_start_time
        
        # Convert current seconds back to h:m:s
        self.simulated_hour = current_seconds // 3600
        self.simulated_minute = (current_seconds % 3600) // 60
        self.simulated_second = current_seconds % 60
        
        # Update display
        self.controller.display.display_two_lines(
            "Time Factor:", 
            f"{factor}x speed"
        )
        
        print(f"Time factor set to {factor}x")
        time.sleep(1)
    
    def update_simulated_time(self):
        """Update the simulated time based on elapsed real time and time factor"""
        if not self.use_simulated_time:
            return
        
        current_time = time.time()
        elapsed_real_seconds = current_time - self.last_update_time
        self.last_update_time = current_time
        
        # Calculate simulated seconds elapsed
        elapsed_sim_seconds = elapsed_real_seconds * self.time_factor
        
        # Update simulated time
        total_seconds = self.simulated_second + elapsed_sim_seconds
        self.simulated_second = total_seconds % 60
        
        total_minutes = self.simulated_minute + (total_seconds // 60)
        self.simulated_minute = total_minutes % 60
        
        total_hours = self.simulated_hour + (total_minutes // 60)
        self.simulated_hour = total_hours % 24
    
    def get_current_time_seconds(self):
        """Get current time of day in seconds (real or simulated)"""
        if self.use_simulated_time:
            # Update simulated time first
            self.update_simulated_time()
            
            # Convert h:m:s to seconds since midnight
            return (self.simulated_hour * 3600 + 
                   self.simulated_minute * 60 + 
                   int(self.simulated_second))
        else:
            # Use real system time
            t = time.localtime()
            return t[3] * 3600 + t[4] * 60 + t[5]
    
    def format_time(self, seconds):
        """Format seconds since midnight to HH:MM format"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours:02d}:{minutes:02d}"
    
    def check_phone_presence(self):
        """Check if phone is present and handle logic"""
        current_time = self.get_current_time_seconds()
        
        # Only enforce phone presence after sleep time
        if current_time > self.sleep_time or current_time < self.wake_time:
            # Check if phone is on the RFID sensor
            if not self.controller.rfid.is_card_present():
                # Alert user to place phone on the RFID sensor
                if not self.night_mode:
                    self.controller.display.display_two_lines("Phone Missing", "Place on sensor")
                    self.controller.actuators.rgb_red()
                    self.controller.actuators.buzzer_beep(220, 0.5)
                return False
            else:
                # Phone is present, verify it's authorized
                if self.controller.rfid.check_card():
                    card_id = self.controller.rfid.get_card_uid_sum()
                    if self.controller.rfid.is_card_authorized():
                        # Phone is authorized, night mode can begin
                        if not self.night_mode:
                            self.activate_night_mode()
                        return True
        
        return self.night_mode
    
    def check_coffee_request(self):
        """Handle coffee button press based on time restrictions"""
        current_time = self.get_current_time_seconds()
        
        # Check if coffee button (left button) is pressed
        if self.controller.sensors.is_button1_pressed() and not self.coffee_tracker.brewing:
            # Wait for button release
            while self.controller.sensors.is_button1_pressed():
                time.sleep(0.01)
            
            # Coffee is not restricted before 5 PM
            if current_time < self.coffee_cutoff_soft:
                self.controller.display.display_two_lines("Brewing Coffee", "Please wait...")
                self.coffee_tracker.brew_coffee()
                return True
            
            # Hard cutoff after 6 PM
            elif current_time >= self.coffee_cutoff_hard:
                self.controller.display.display_two_lines("Coffee Denied", "Too late for caffeine")
                self.coffee_tracker.deny_coffee()
                return False
            
            # Warning zone between 5-6 PM
            else:
                # If warning was already shown and within timeout, proceed brewing
                if (self.coffee_warning_active and 
                    time.time() - self.coffee_warning_time < self.coffee_double_confirm_timeout):
                    
                    self.coffee_warning_active = False
                    self.controller.display.display_two_lines("Brewing Coffee", "Please wait...")
                    self.coffee_tracker.brew_coffee()
                    return True
                
                # Show warning and set status
                else:
                    self.coffee_warning_active = True
                    self.coffee_warning_time = time.time()
                    self.controller.display.display_two_lines("Coffee after 5PM", "Press again to confirm")
                    self.controller.actuators.rgb_red()
                    self.controller.actuators.buzzer_beep(440, 0.2)
                    time.sleep(0.2)
                    self.controller.actuators.buzzer_beep(440, 0.2)
                    time.sleep(2)
                    self.controller.actuators.rgb_off()
                    return False
        
        # Reset warning after timeout
        if self.coffee_warning_active and time.time() - self.coffee_warning_time >= self.coffee_double_confirm_timeout:
            self.coffee_warning_active = False
        
        return False
    
    def activate_night_mode(self):
        """Activate night mode - secure home, turn off appliances"""
        if self.night_mode:
            return
        
        print("Activating night mode")
        self.night_mode = True
        
        # Display message
        self.controller.display.display_two_lines("Night Mode", "Activated")
        
        # Lock window and door
        self.controller.actuators.door_close()
        self.controller.actuators.window_close()
        
        # Turn off lights
        self.light.lights_off()
        
        # Turn off fan if available
        if hasattr(self.controller.actuators, 'fan_available') and self.controller.actuators.fan_available:
            self.controller.actuators.fan_set_speed(0)
        
        # Visual and audio feedback
        self.controller.actuators.rgb_blue(30)  # Dim blue for night
        self.controller.actuators.buzzer_beep(880, 0.2)
        time.sleep(0.2)
        self.controller.actuators.buzzer_beep(660, 0.2)
        time.sleep(2)
        
        # Initial sleep environment optimization
        self.optimize_sleep_environment()
    
    def deactivate_night_mode(self):
        """Deactivate night mode at wake-up time"""
        if not self.night_mode:
            return
        
        print("Deactivating night mode")
        self.night_mode = False
        
        # Display message
        self.controller.display.display_two_lines("Good Morning", "Wake-up time!")
        
        # Open window for fresh air
        self.controller.actuators.window_open(50)  # Half-open for ventilation
        
        # Turn on lights
        self.light.lights_on(100)  # Full brightness
        
        # Visual and audio feedback
        self.controller.actuators.rgb_green()
        self.controller.actuators.buzzer_beep(660, 0.2)
        time.sleep(0.2)
        self.controller.actuators.buzzer_beep(880, 0.2)
        time.sleep(1)
        self.controller.actuators.rgb_off()
    
    def optimize_sleep_environment(self):
        """Monitor and adjust temperature and humidity for optimal sleep"""
        if not self.night_mode:
            return
        
        # Read current temperature and humidity
        temp, humidity = self.controller.sensors.read_temperature_humidity()
        print(f"Sleep environment: {temp}°C, {humidity}%")
        
        # Show current conditions
        self.controller.display.display_two_lines(
            f"Temp: {temp}°C", 
            f"Humidity: {humidity}%"
        )
        
        # Temperature regulation
        if temp > self.optimal_sleep_temp + 2:
            # Too hot - turn on fan if available
            if hasattr(self.controller.actuators, 'fan_available') and self.controller.actuators.fan_available:
                fan_speed = min(100, max(0, (temp - self.optimal_sleep_temp) * 25))  # Scale fan speed
                self.controller.actuators.fan_set_speed(fan_speed)
                print(f"Fan set to {fan_speed}%")
            
            # If still too hot or humidity is high, open window
            if temp > self.optimal_sleep_temp + 4 or humidity > self.max_sleep_humidity:
                window_percent = min(100, max(0, (temp - self.optimal_sleep_temp - 2) * 25))
                self.controller.actuators.window_open(window_percent)
                print(f"Window opened to {window_percent}%")
        else:
            # Temperature is good - turn off fan
            if hasattr(self.controller.actuators, 'fan_available') and self.controller.actuators.fan_available:
                self.controller.actuators.fan_set_speed(0)
            
            # Close window if humidity is not an issue
            if humidity <= self.max_sleep_humidity:
                self.controller.actuators.window_close()
    
    def handle_night_disturbance(self):
        """Handle motion detection during night mode"""
        if not self.night_mode:
            return
        
        # Check for motion during night
        if self.controller.sensors.is_motion_detected():
            print("Motion detected in night mode")
            
            # Display calming message
            self.controller.display.display_two_lines("Motion Detected", "Relax and sleep")
            
            # Soothing light and sound
            self.controller.actuators.rgb_blue(10)  # Very dim blue
            
            # Play a gentle lullaby tune
            self.play_lullaby()
            
            # Return to darkness
            time.sleep(3)
            self.controller.actuators.rgb_off()
    
    def play_lullaby(self):
        """Play a gentle lullaby to help user go back to sleep"""
        # Simple lullaby notes (Brahms' Lullaby)
        notes = [
            (392, 0.5), (440, 0.5), (392, 0.5), (294, 0.5),
            (349, 0.5), (349, 0.5), (294, 1.0),
            (392, 0.5), (440, 0.5), (392, 0.5), (294, 0.5),
            (349, 0.5), (349, 0.5), (294, 1.0),
            (294, 0.5), (494, 0.5), (440, 0.5), (349, 0.5),
            (392, 0.5), (392, 0.5), (349, 0.5), (294, 0.5),
            (294, 0.5), (494, 0.5), (440, 0.5), (349, 0.5),
            (392, 0.5), (349, 0.5), (294, 1.0)
        ]
        
        # Play the lullaby
        for note, duration in notes:
            self.controller.actuators.buzzer.freq(note)
            self.controller.actuators.buzzer.duty(300)  # Quiet volume
            time.sleep(duration * 0.5)  # Play shorter to not disturb too much
            self.controller.actuators.buzzer.duty(0)
            time.sleep(0.05)
        
        # Ensure buzzer is off
        self.controller.actuators.buzzer.duty(0)
    
    def handle_sleep_time_reminder(self):
        """Handle pre-sleep reminders and light dimming"""
        current_time = self.get_current_time_seconds()
        
        # Check if it's pre-sleep time (between 1 hour before sleep and sleep time)
        if self.pre_sleep_time <= current_time < self.sleep_time:
            progress = (current_time - self.pre_sleep_time) / 3600  # 0 to 1 over one hour
            
            # Gradually dim lights
            brightness = 100 - (progress * 100)
            self.light.set_brightness(brightness)
            
            # Every 10 minutes, show reminder
            minutes_since_pre_sleep = (current_time - self.pre_sleep_time) // 60
            if minutes_since_pre_sleep % 10 == 0 and minutes_since_pre_sleep > 0:
                time_to_sleep = (self.sleep_time - current_time) // 60
                self.controller.display.display_two_lines(
                    "Sleep Reminder",
                    f"{time_to_sleep} mins left"
                )
                # Gentle reminder sound
                self.controller.actuators.buzzer_beep(660, 0.2)
                time.sleep(0.2)
                self.controller.actuators.buzzer_beep(440, 0.2)
                time.sleep(3)  # Show message for 3 seconds
        
        # At sleep time, remind user until phone is placed
        elif current_time >= self.sleep_time and not self.night_mode:
            self.controller.display.display_two_lines(
                "Sleep Time!",
                "Place phone on sensor"
            )
            if int(time.time()) % 30 < 1:  # Remind every 30 seconds
                self.controller.actuators.rgb_red()
                self.controller.actuators.buzzer_beep(440, 0.3)
                time.sleep(0.3)
                self.controller.actuators.buzzer_beep(330, 0.3)
                time.sleep(3)
                self.controller.actuators.rgb_off()
    
    def handle_morning_wake_up(self):
        """Handle morning wake-up routine"""
        current_time = self.get_current_time_seconds()
        
        # Check if it's pre-wake time
        if self.pre_wake_time <= current_time < self.wake_time:
            # If night mode still active, start wake-up routine
            if self.night_mode:
                progress = (current_time - self.pre_wake_time) / 3600  # 0 to 1 over one hour
                
                # Gradually open window for fresh air
                window_percent = progress * 50  # Open to 50% max
                self.controller.actuators.window_open(window_percent)
                
                # Gradually increase light
                brightness = progress * 100
                self.light.set_brightness(brightness)
                
                # Display the wake-up progress
                time_to_wake = (self.wake_time - current_time) // 60
                self.controller.display.display_two_lines(
                    "Good Morning Soon",
                    f"Wake in {time_to_wake} mins"
                )
        
        # At wake time, end night mode
        elif current_time >= self.wake_time and current_time < self.wake_time + 300:  # Within 5 minutes
            if self.night_mode:
                self.deactivate_night_mode()
    
    def run(self):
        """Main run loop for the Smart Sleep Assistant"""
        print("Smart Sleep Assistant running...")
        
        # Add default authorized RFID cards (phones)
        self.controller.rfid.add_authorized_card(668, "James")
        self.controller.rfid.add_authorized_card(383, "Eric")
        
        # If simulation is enabled, print simulation controls
        if self.use_simulated_time:
            print("\nSIMULATION MODE ACTIVE")
            print(f"Time acceleration factor: {self.time_factor}x")
            print("Use Button 1 (left) to increase time by 1 hour")
            print("Use Button 2 (right) to speed up time (2x, 10x, 60x, 1x)")
            print("Initial simulated time:", self.format_time(self.get_current_time_seconds()))
        
        try:
            while True:
                # Get current time
                current_time = self.get_current_time_seconds()
                current_time_formatted = self.format_time(current_time)
                
                # Simulation controls (when enabled)
                if self.use_simulated_time:
                    # Button 1 (left): Advance time by 1 hour
                    if self.controller.sensors.is_button1_pressed():
                        self.simulated_hour = (self.simulated_hour + 1) % 24
                        self.controller.display.display_two_lines(
                            "Time Advanced:", 
                            f"{self.format_time(self.get_current_time_seconds())}"
                        )
                        time.sleep(0.5)  # Debounce
                    
                    # Button 2 (right): Cycle time acceleration: 1x → 2x → 10x → 60x → 1x
                    if self.controller.sensors.is_button2_pressed():
                        if self.time_factor == 1:
                            self.set_time_factor(2)
                        elif self.time_factor == 2:
                            self.set_time_factor(10)
                        elif self.time_factor == 10:
                            self.set_time_factor(60)
                        else:
                            self.set_time_factor(1)
                        time.sleep(0.5)  # Debounce
                
                # Check for coffee requests
                self.check_coffee_request()
                
                # Handle phone presence check and night mode activation
                self.check_phone_presence()
                
                # Handle sleep time reminders
                self.handle_sleep_time_reminder()
                
                # Handle morning wake-up routine
                self.handle_morning_wake_up()
                
                # In night mode, check for disturbances and optimize environment
                if self.night_mode:
                    self.handle_night_disturbance()
                    
                    # Periodically optimize sleep environment (every 5 minutes)
                    if int(time.time()) % 300 < 1:
                        self.optimize_sleep_environment()
                
                # Display current system status if no other message is showing
                if not self.coffee_warning_active and not self.coffee_tracker.brewing:
                    if self.night_mode:
                        # Include SIM indicator if using simulated time
                        time_label = f"SIM {current_time_formatted}" if self.use_simulated_time else current_time_formatted
                        self.controller.display.display_two_lines(
                            f"Night Mode {time_label}",
                            "Sleep well!"
                        )
                    else:
                        sleep_time_formatted = self.format_time(self.sleep_time)
                        # Include SIM indicator if using simulated time
                        time_label = f"SIM {current_time_formatted}" if self.use_simulated_time else current_time_formatted
                        self.controller.display.display_two_lines(
                            f"Time: {time_label}",
                            f"Sleep: {sleep_time_formatted}"
                        )
                
                # Short delay to prevent tight loop
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("Smart Sleep Assistant stopped")
            # Cleanup
            self.light.lights_on(100)
            self.controller.actuators.window_close()
            self.controller.actuators.door_close()
            self.controller.actuators.rgb_off()
            self.controller.actuators.buzzer_off()

# Run the Smart Sleep Assistant if script is executed directly
if __name__ == "__main__":
    # Create the Smart Sleep Assistant with simulation enabled
    # Parameters:
    #   use_simulated_time: Enable time simulation (True/False)
    #   time_factor: How fast simulated time passes (1x = real time, 60x = 1 minute per second)
    ssa = SmartSleepAssistant(use_simulated_time=True, time_factor=10)
    
    # Set initial simulated time (24-hour format)
    ssa.set_simulated_time(hour=16, minute=45)  # Set to 4:45 PM
    
    # Run the assistant
    ssa.run()