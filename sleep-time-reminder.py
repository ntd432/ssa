# This file sends a reminder to the user to go to bed at a specified time. It uses the `datetime` module to get the current time and the `smtplib` module to send an email reminder. The script runs in an infinite loop, checking the current time every minute and sending an email if it's time to go to bed.

import datetime
import time
from display_manager import DisplayManager as display_manager

def display_message(message):
    # Function to display a message (e.g., on a screen or console)
    display_manager.display_scroolling_text(message)  # Replace with actual display logic

def dim_led_light():
    # Function to dim the LED light
    display_manager.display_text("Dimming LED light...")  # Replace with actual LED control logic

def simulate_time():
    # Simulated time starts at 10:00 PM
    simulated_time = datetime.datetime.combine(datetime.date.today(), datetime.time(22, 0))
    while True:
        yield simulated_time.time()
        simulated_time += datetime.timedelta(minutes=15)  # 1 second = 15 minutes

def send_sleep_reminder():
    sleep_time = datetime.time(23, 0)  # 11:00 PM
    reminder_time = datetime.time(22, 30)  # 10:30 PM
    dim_time = datetime.time(22, 45)  # 10:45 PM

    simulated_clock = simulate_time()

    for now in simulated_clock:
        print(f"Simulated Time: {now}")  # Display the simulated time for debugging

        if now >= reminder_time and now < dim_time:
            display_message("Reminder: It's time to start preparing for bed!")
        elif now >= dim_time and now < sleep_time:
            dim_led_light()
        elif now >= sleep_time:
            display_message("It's 11:00 PM. Time to go to bed!")
            break  # Exit the loop after sending the final reminder

        time.sleep(1)  # Simulate the passage of 15 minutes in 1 second

if __name__ == "__main__":
    send_sleep_reminder()
