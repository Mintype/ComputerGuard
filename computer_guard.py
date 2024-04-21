from win10toast import ToastNotifier
import keyboard
import ctypes
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from playsound import playsound
import os
import cv2
import threading
import time
import tkinter as tk
from PIL import Image, ImageTk

# Global variables
activated = False
exit_flag = False
root = None
canvas = None
image_label = None

# create a threading lock
activated_lock = threading.Lock()

# function to take a picture
def take_picture():
    # open default camera
    cap = cv2.VideoCapture(0)

    # check if the camera is opened correctly
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    s, im = cap.read() # captures image
    cv2.imwrite("intruder.bmp", im) # writes image test.bmp to disk

    # Release the camera
    cap.release()

# function to play an alert sound
def play_alert_sound(sound_file):
    # Play the sound
    playsound(sound_file, block=False)

# function to set the system volume
def set_system_volume(volume):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume_interface = cast(interface, POINTER(IAudioEndpointVolume))
    volume_interface.SetMasterVolumeLevelScalar(volume, None)

# function to create and display GUI
def create_and_display_gui(image_path):
    global root, canvas, image_label

    # create GUI
    root = tk.Tk()

    # maximize the window
    root.attributes('-fullscreen', True)

    # create a canvas
    canvas = tk.Canvas(root)
    canvas.pack(fill="both", expand=True)

    # load and display the image
    image = Image.open(image_path)
    image = ImageTk.PhotoImage(image)

    image_label = tk.Label(canvas, image=image)
    image_label.image = image
    image_label.pack(fill="both", expand=True)

    # display the GUI
    root.mainloop()

def activate():
    print("Activating...")

    # display a notification to the intruder
    # display_notification("INTRUDER ALERT SYSTEM", "INTRUDER HAS ACTIVATED THE ALERT SYSTEM!")

    # set volume to maximum (1.0)
    set_system_volume(1.0)

    # play an alert sound
    play_alert_sound("sound_effects/alert_sound.mp3")
    playsound("sound_effects/alert_sound.mp3", block=False)
    
    # take a picture of the intruder
    take_picture()

    # alert_thread = threading.Thread(target=play_alert_sound, args=("sound_effects/alert_sound.mp3",))
    # alert_thread.start()

    # create and display GUI
        # create GUI

    root = tk.Tk()

    # maximize the window
    root.attributes('-fullscreen', True)

    try:
        # create a canvas
        canvas = tk.Canvas(root)
        canvas.pack(fill="both", expand=True)

        # load and display the image
        image = Image.open("intruder.bmp")
        image = ImageTk.PhotoImage(image)

        image_label = tk.Label(canvas, image=image)
        image_label.image = image
        image_label.pack(fill="both", expand=True)
    except:
        pass

    root.attributes('-topmost', True)

    # display the GUI
    root.mainloop()


# function to be called when a key is pressed
def on_key_press(event):
    global activated
    print("A key was pressed:", event.name)
    if(not activated):
        if event.name == "esc":
            activated = False
            keyboard.unhook_all()
            exit(0)
        else:
            activated = True
            # activate()
            activate_thread = threading.Thread(target=activate)
            activate_thread.start()
    # print("Activated:", activated)

# display a windows toast notification
def display_notification(title, message):
    toaster = ToastNotifier()
    toaster.show_toast(title, message, duration=1)

# main function
def main():

    display_notification("Intruder Alert System", "Intruder Alert System is running.")

    # start the keyboard listener thread
    # keyboard_thread = threading.Thread(target=keyboard_listener)
    # keyboard_thread.start()

    print("Listening for key presses...")
    keyboard.on_press(on_key_press)
    keyboard.wait("esc") # execution will pause here until the "esc" key is pressed

if __name__ == "__main__":
    main()