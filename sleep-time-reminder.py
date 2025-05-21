# This file sends a reminder to the user to go to bed at a specified time. It uses the `datetime` module to get the current time and the `smtplib` module to send an email reminder. The script runs in an infinite loop, checking the current time every minute and sending an email if it's time to go to bed.

import time
from display_manager import DisplayManager as display_manager

def display_message(message):
    # Function to display a message (e.g., on a screen or console)
    display_manager.display_scroolling_text(message)  # Replace with actual display logic

def dim_led_light():
    # Function to dim the LED light
    display_manager.display_text("Dimming LED light...")  # Replace with actual LED control logic

def simulate_time():
    # Simulated time starts at 10:00 PM (22:00)
    simulated_hour = 22
    simulated_minute = 0
    while True:
        yield simulated_hour, simulated_minute
        simulated_minute += 10  # Increment by 10 minutes (1 second = 10 minutes)
        if simulated_minute >= 60:
            simulated_minute = 0
            simulated_hour += 1

def send_sleep_reminder():
    reminder_hour, reminder_minute = 22, 30  # 10:30 PM
    dim_hour, dim_minute = 22, 50  # 10:50 PM
    sleep_hour, sleep_minute = 23, 0  # 11:00 PM

    simulated_clock = simulate_time()

    for hour, minute in simulated_clock:
        print(f"Simulated Time: {hour:02}:{minute:02}")  # Display the simulated time for debugging

        if (hour == reminder_hour and minute == reminder_minute):
            display_message("Reminder: It's time to start preparing for bed!")
        elif (hour == dim_hour and minute == dim_minute):
            dim_led_light()
        elif (hour == sleep_hour and minute == sleep_minute):
            display_message("It's 11:00 PM. Time to go to bed!")
            break  # Exit the loop after sending the final reminder

        time.sleep(1)  # Simulate the passage of 10 minutes in 1 second

if __name__ == "__main__":
    send_sleep_reminder()
