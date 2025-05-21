import network
import time
import urequests

# Default network settings
DEFAULT_SSID = "Google Pixel 8 Pro"
DEFAULT_PASSWORD = "Matebook17"
DEFAULT_SERVER_URL = "http://yourserver.com/api/data"

class WebManager:
    def __init__(self, ssid=DEFAULT_SSID, password=DEFAULT_PASSWORD):
        self.ssid = ssid
        self.password = password
        self.server_url = DEFAULT_SERVER_URL
        self.wlan = network.WLAN(network.STA_IF)
        self.is_connected = False
    
    def connect(self, timeout=20):
        """Connect to WiFi network
        Args:
            timeout: Maximum connection time in seconds
        Returns:
            bool: True if connection successful, False otherwise
        """
        print("Connecting to WiFi...")
        
        # Activate WiFi interface
        self.wlan.active(True)
        
        # Check if already connected
        if self.wlan.isconnected():
            print("Already connected to WiFi")
            self.is_connected = True
            print("Network config:", self.wlan.ifconfig())
            return True
        
        # Connect to network
        try:
            self.wlan.connect(self.ssid, self.password)
            
            # Wait for connection with timeout
            start_time = time.time()
            while not self.wlan.isconnected():
                if time.time() - start_time > timeout:
                    print("WiFi connection timeout")
                    return False
                time.sleep(0.5)
            
            self.is_connected = True
            print("Connected to WiFi")
            print("Network config:", self.wlan.ifconfig())
            return True
        
        except Exception as e:
            print("WiFi connection error:", e)
            return False
    
    def disconnect(self):
        """Disconnect from WiFi network"""
        if self.wlan.active():
            self.wlan.disconnect()
            self.is_connected = False
            print("Disconnected from WiFi")
    
    def is_wifi_connected(self):
        """Check if connected to WiFi
        Returns:
            bool: True if connected, False otherwise
        """
        return self.wlan.isconnected()
    
    def set_server_url(self, url):
        """Set server URL for API requests
        Args:
            url: Server URL
        """
        self.server_url = url
    
    def send_data(self, data, endpoint=None):
        """Send data to server
        Args:
            data: Dictionary of data to send
            endpoint: Optional API endpoint to append to server URL
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.is_wifi_connected():
            print("Not connected to WiFi")
            return False
        
        url = self.server_url
        if endpoint:
            url += "/" + endpoint
        
        try:
            print(f"Sending data to {url}")
            response = urequests.post(
                url,
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                print("Data sent successfully")
                response.close()
                return True
            else:
                print(f"Server error: {response.status_code}")
                response.close()
                return False
                
        except Exception as e:
            print("Error sending data:", e)
            return False
    
    def get_data(self, endpoint=None):
        """Get data from server
        Args:
            endpoint: Optional API endpoint to append to server URL
        Returns:
            dict: Response data or None if failed
        """
        if not self.is_wifi_connected():
            print("Not connected to WiFi")
            return None
        
        url = self.server_url
        if endpoint:
            url += "/" + endpoint
        
        try:
            print(f"Getting data from {url}")
            response = urequests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                response.close()
                return data
            else:
                print(f"Server error: {response.status_code}")
                response.close()
                return None
                
        except Exception as e:
            print("Error getting data:", e)
            return None