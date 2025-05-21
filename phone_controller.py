from display_manager import DisplayManager
from rfid_manager import RFIDManager
import time, threading

CONFIGURED_SLEEP_TIME = 23 * 3600

class PhoneController:
    def __init__(self):
        self.display = DisplayManager()
        self.controlled = False
        self.rfid = RFIDManager()

    def get_current_time_seconds():
        """Get current time of day in seconds"""
        t = time.localtime()
        return t[3] * 3600 + t[4] * 60 + t[5]

    def display_message(self):
        while not self.controlled:
            current_time = self.get_current_time_seconds()
            if current_time > CONFIGURED_SLEEP_TIME and not self.controlled:
                self.display.display_two_lines("Time to sleep", "Put your phone here")
            self.actuators.rgb_red()
            self.actuators.buzzer_beep(220, 0.5)
            time.sleep(0.1)
    
    def check_phone(self):
        if self.rfid.check_card():
            card_id = self.rfid.get_card_id()
            self.display.display_two_lines("Phone Detected", card_id[:16])
            
            # Check if this is an authorized card
            if self.rfid.is_card_authorized():
                name = self.rfid.get_authorized_card_name()
                self.display.display_two_lines(f"Good night {name}", "See you tomorrow")
                
                # Visual and audio feedback
                self.actuators.rgb_green()
                self.actuators.buzzer_beep(880, 0.1)

                print(f"Done for card: {card_id}")
                self.controlled = True
                self.actuators.buzzer_off()
                
                # Wait a moment to prevent multiple scans
                time.sleep(0.5)
            else:
                self.display.display_two_lines("Wrong phone", "Don't cheat")
                
                # Visual and audio feedback for denied access
                self.actuators.rgb_red()
                for _ in range(2):  # Two quick error beeps
                    self.actuators.buzzer_beep(220, 0.2)
                    time.sleep(0.1)
                
                print(f"Denied for card: {card_id}")
                time.sleep(1)
                self.actuators.rgb_off()

    def enforce_routine(self):
        t1 = threading.Thread(target=self.display_message)
        t2 = threading.Thread(target=self.check_phone)

        t1.start()
        t2.start()

def main_loop():
    """Main system loop"""
    controller = PhoneController()
    
    while True:
        controller.enforce_routine()
        
if __name__ == "__main__":
    main_loop()

    
        