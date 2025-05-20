import network
import time
import json

WIFI_SSID = "YourWiFi"
WIFI_PASS = "YourPassword"
SERVER_URL = "http://yourserver.com/api/sleep-tracker"

def init():
    """Initialize network connection"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            time.sleep(1)
    print("WiFi connected:", wlan.ifconfig())

def send_sleep_data(sleep_data):
    """Send sleep-related data to server"""
    try:
        data = {
            "timestamp": time.time(),
            "sleep_quality": sleep_data.get("quality", 0),
            "awakenings": sleep_data.get("awakenings", 0),
            "time_to_sleep": sleep_data.get("time_to_sleep", 0),
            "sleep_start": sleep_data.get("sleep_start", 0),
            "sleep_end": sleep_data.get("sleep_end", 0)
        }
        # In a real implementation, we'd send this via HTTP
        print("Sleep data:", data)
    except Exception as e:
        print("Failed to send sleep data:", e)