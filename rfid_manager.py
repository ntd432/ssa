from machine import UART, Pin, I2C
import time
from mfrc522_i2c import mfrc522  # Make sure this library is available

# Constants for I2C communication with MFRC522
I2C_ADDR = 0x28     # Default I2C address for MFRC522
PIN_SCL = 22        # SCL pin for I2C
PIN_SDA = 21        # SDA pin for I2C

class RFIDManager:
    """RFID Manager for MFRC522 module using I2C interface"""
    
    def __init__(self):
        """Initialize RFID reader with I2C interface"""
        try:
            # Initialize MFRC522 with I2C
            self.rc522 = mfrc522(PIN_SCL, PIN_SDA, I2C_ADDR)
            self.rc522.PCD_Init()
            self.rc522.ShowReaderDetails()
            
            # Store state
            self.last_scan_time = 0
            self.last_card_id = None
            self.card_uid_bytes = None
            self.authorized_cards = {}  # Dictionary to store authorized card IDs
            
            print("RFID manager initialized successfully")
            self.is_connected = True
            
        except Exception as e:
            print(f"Error initializing RFID manager: {e}")
            self.is_connected = False
    
    def check_card(self):
        """Check if a new card is present
        
        Returns:
            bool: True if a card is detected, False otherwise
        """
        if not self.is_connected:
            return False
            
        try:
            # First check if a new card is present
            if not self.rc522.PICC_IsNewCardPresent():
                return False
                
            # Then try to read the card serial
            if not self.rc522.PICC_ReadCardSerial():
                return False
                
            # If we got here, we successfully detected a card
            self.last_scan_time = time.time()
            
            # Get card UID
            self._process_card_data()
            return True
                
        except Exception as e:
            print(f"Error checking RFID card: {e}")
            return False
    
    def _process_card_data(self):
        """Process RFID card data from the MFRC522 reader"""
        try:
            # Store the raw UID bytes
            self.card_uid_bytes = self.rc522.uid.uidByte[0 : self.rc522.uid.size]
            
            # Convert UID bytes to string format
            uid_sum = 0
            uid_parts = []
            
            for i in self.card_uid_bytes:
                uid_sum += i
                uid_parts.append(str(i))
            
            # Create card ID string (two formats available)
            self.last_card_id = "-".join(uid_parts)  # Format like "84-12-125-63"
            self.last_card_uid_sum = uid_sum         # Sum of UID bytes (like in example)
            
            print(f"Card detected: {self.last_card_id} (Sum: {self.last_card_uid_sum})")
            
            # Check if this is an authorized card
            if self.is_card_authorized():
                name = self.get_authorized_card_name()
                print(f"Authorized: {name}")
            else:
                print("Unauthorized card")
                
        except Exception as e:
            print(f"Error processing card data: {e}")
    
    def get_card_id(self):
        """Get the ID of the last scanned card
        
        Returns:
            str: Card ID or None if no card scanned
        """
        return self.last_card_id
    
    def get_card_uid_sum(self):
        """Get the sum of UID bytes (as used in the example code)
        
        Returns:
            int: Sum of UID bytes or None if no card scanned
        """
        return self.last_card_uid_sum
    
    def time_since_last_scan(self):
        """Get time in seconds since last card scan
        
        Returns:
            float: Seconds since last scan, or infinity if no scan yet
        """
        if self.last_scan_time == 0:
            return float('inf')
        return time.time() - self.last_scan_time
    
    def add_authorized_card(self, card_id, name):
        """Add a card to the authorized cards list
        
        Args:
            card_id: Card ID to authorize (can be string ID or UID sum)
            name: Name or description for this card
        """
        self.authorized_cards[str(card_id)] = name
        print(f"Added authorized card: {name} ({card_id})")
    
    def remove_authorized_card(self, card_id):
        """Remove a card from the authorized cards list
        
        Args:
            card_id: Card ID to remove
        
        Returns:
            bool: True if card was removed, False if not found
        """
        card_id_str = str(card_id)
        if card_id_str in self.authorized_cards:
            name = self.authorized_cards.pop(card_id_str)
            print(f"Removed authorized card: {name} ({card_id})")
            return True
        return False
    
    def is_card_authorized(self, card_id=None):
        """Check if a card is authorized
        
        Args:
            card_id: Card ID to check, or None to use last scanned card
        
        Returns:
            bool: True if authorized, False otherwise
        """
        if card_id is None:
            # Check both formats - string ID and UID sum
            if self.last_card_id and str(self.last_card_id) in self.authorized_cards:
                return True
            if self.last_card_uid_sum and str(self.last_card_uid_sum) in self.authorized_cards:
                return True
            return False
            
        return str(card_id) in self.authorized_cards
    
    def get_authorized_card_name(self, card_id=None):
        """Get the name associated with an authorized card
        
        Args:
            card_id: Card ID to check, or None to use last scanned card
        
        Returns:
            str: Card name or None if not authorized
        """
        if card_id is None:
            # Try string format first
            if self.last_card_id and str(self.last_card_id) in self.authorized_cards:
                return self.authorized_cards[str(self.last_card_id)]
            # Then try UID sum format
            if self.last_card_uid_sum and str(self.last_card_uid_sum) in self.authorized_cards:
                return self.authorized_cards[str(self.last_card_uid_sum)]
            return None
            
        card_id_str = str(card_id)
        if card_id_str in self.authorized_cards:
            return self.authorized_cards[card_id_str]
        return None
    
    def wait_for_card(self, timeout=None):
        """Wait for a card to be presented
        
        Args:
            timeout: Timeout in seconds, or None to wait indefinitely
        
        Returns:
            str: Card ID if detected, None if timeout
        """
        print("Waiting for RFID card...")
        
        start_time = time.time()
        while True:
            if self.check_card():
                return self.last_card_id
                
            # Check for timeout
            if timeout is not None and time.time() - start_time > timeout:
                print("Card scan timeout")
                return None
                
            time.sleep(0.1)  # Short delay to prevent tight loop

# Simple demo to test the RFID manager with the MFRC522 I2C interface
def rfid_demo():
    """Stand-alone demo for RFID reader"""
    from machine import Pin, PWM
    import time
    
    # Create LED for visual feedback
    led = Pin(12, Pin.OUT)
    
    # Create servo for door control
    servo = PWM(Pin(13))
    servo.freq(50)
    
    # Initialize RFID manager
    rfid = RFIDManager()
    
    # Add some test authorized cards - use the UID sum format from example
    rfid.add_authorized_card(510, "Admin Card")  # This matches the example code's card
    rfid.add_authorized_card(600, "Guest Card")  # Another example
    
    print("RFID Demo: Present a card to the reader")
    
    try:
        while True:
            if rfid.check_card():
                card_uid_sum = rfid.get_card_uid_sum()
                print(f"Card detected with UID sum: {card_uid_sum}")
                
                if rfid.is_card_authorized():
                    # Authorized card - open door
                    name = rfid.get_authorized_card_name()
                    print(f"Access granted to {name}")
                    led.value(1)
                    servo.duty(128)  # Open door (180 degrees)
                    print("Door opened")
                else:
                    # Unauthorized card - blink LED rapidly
                    print("Access denied")
                    for _ in range(5):
                        led.value(1)
                        time.sleep(0.1)
                        led.value(0)
                        time.sleep(0.1)
            
            # Check if button is pressed to close door
            button1 = Pin(16, Pin.IN, Pin.PULL_UP)
            if button1.value() == 0:  # Button pressed (active low)
                servo.duty(25)  # Close door (0 degrees)
                led.value(0)
                print("Door closed")
            
            time.sleep(0.1)  # Short delay between checks
            
    except KeyboardInterrupt:
        print("Demo stopped")
        servo.duty(25)  # Make sure door is closed
        led.value(0)

# Run the demo if this script is executed directly
if __name__ == "__main__":
    rfid_demo()