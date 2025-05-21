from display_manager import DisplayManager
from actuator_manager import ActuatorManager
from rfid_manager import RFIDManager
import time

CONFIGURED_SLEEP_TIME = 11 * 3600
CARD_ID_DICT = {668: "James", 383: "Eric"}

class PhoneController:
    def __init__(self):
        self.display = DisplayManager()
        self.actuators = ActuatorManager()
        self.controlled = False
        self.rfid = RFIDManager()

    def get_current_time_seconds(self):
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
            self.check_phone()
    
    def check_phone(self):
        if self.rfid.check_card():
            card_id = self.rfid.get_card_uid_sum()
            self.display.display_text(f"Phone Detected: {card_id}")
            time.sleep(2)
            
            # Check if this is an authorized card
            if card_id in CARD_ID_DICT.keys():
                name = CARD_ID_DICT[card_id]
                self.display.display_two_lines(f"Good night {name if name else ''}", "See you tomorrow")
                
                # Visual and audio feedback
                self.actuators.rgb_green()
                self.actuators.buzzer_beep(880, 0.1)

                print(f"Done for card: {card_id}")
                self.controlled = True
                self.actuators.buzzer_off()
                self.actuators.rgb_off()
                
                # Wait a moment to prevent multiple scans
            else:
                self.display.display_two_lines("Wrong phone", "Don't cheat")
                self.controlled = False
                # Visual and audio feedback for denied access
                self.actuators.rgb_red()
                for _ in range(2):  # Two quick error beeps
                    self.actuators.buzzer_beep(220, 0.2)
                    time.sleep(0.1)
                
                print(f"Denied for card: {card_id}")
                time.sleep(1)
                self.actuators.rgb_off()
        else:
            self.controlled = False

    def enforce_routine(self):
        self.display_message()

def main_loop():
    """Main system loop"""
    controller = PhoneController()
    
    while True:
        controller.enforce_routine()
        controller.controlled = False
        
if __name__ == "__main__":
    main_loop()

    
        