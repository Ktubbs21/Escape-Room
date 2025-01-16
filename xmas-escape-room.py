import tkinter as tk
import tkinter.font as tkFont
import threading
import pygame  # For sound playback

# Initialize pygame mixer for sound
pygame.mixer.init()

# Initialize the main Tkinter window
root = tk.Tk()
root.title("Escape Room Countdown Clock")

# Initialize custom fonts (after root is created)
timer_font = tkFont.Font(family="Montserrat", size=260)
clue_font = tkFont.Font(family="Cinzel", size=45)

# Function to format time
def format_time(seconds):
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02}:{secs:02}"

# Countdown function
def countdown():
    global countdown_seconds
    if countdown_seconds > 0:
        countdown_seconds -= 1
        time_label.config(text=format_time(countdown_seconds))
        root.after(1000, countdown)  # Call countdown every second
    else:
        time_label.config(text="Time's up!", font=clue_font)  # Use the clue font size for "Time's up!"

# Function to play a sound when message is displayed
def play_sound():
    pygame.mixer.music.load('bling-sound-effect.wav')  # Use .wav, .mp3, or .ogg
    pygame.mixer.music.play()

# Function to display a message and hide the countdown temporarily
def display_message(message):
    play_sound()  # Play a sound when the message is displayed
    time_label.pack_forget()  # Hide the countdown label
    message_label.config(text=message)
    message_label.pack(expand=True)
    root.after(20000, clear_message)  # Clear the message after 20 seconds

# Function to clear the message and show the countdown again
def clear_message():
    message_label.pack_forget()  # Hide the message label
    time_label.pack(expand=True)  # Show the countdown label again

# Function to listen for console input asynchronously
def message_listener():
    while True:
        message = input("Enter a message to display: ")
        display_message(message)

# Function to start the timer
def start_timer(event=None):
    global countdown_running  # Declare the global variable
    if not countdown_running:  # Only start countdown if it's not already running
        countdown_running = True
        logo_label.pack_forget()  # Hide the logo label
        time_label.pack(expand=True)  # Show the countdown label
        countdown()  # Start the countdown

# Set window size (fullscreen disabled)
root.geometry("1920x1080")

# Set initial countdown time (default: 1 hour = 3600 seconds)
countdown_seconds = 3600  # Set desired countdown time here in seconds

# Flag to prevent multiple countdowns
countdown_running = False  # Initially, the countdown is not running

# Create labels for the countdown and the message
time_label = tk.Label(root, text=format_time(countdown_seconds), font=timer_font)
message_label = tk.Label(root, text="", font=clue_font)

# Load the logo image (ensure 'logo.png' is in the same directory or provide the correct path)
logo_image = tk.PhotoImage(file="logo.png")
logo_label = tk.Label(root, image=logo_image)

# Pack the logo label initially
logo_label.pack(expand=True)

# Bind the Enter key to start the timer
root.bind('<Return>', start_timer)

# Run the message listener in a separate thread
listener_thread = threading.Thread(target=message_listener, daemon=True)
listener_thread.start()

# Run the Tkinter main loop
root.mainloop()
