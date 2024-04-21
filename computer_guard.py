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

# Global variables
activated = False
exit_flag = False

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
    playsound(sound_file)

# function to set the system volume
def set_system_volume(volume):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume_interface = cast(interface, POINTER(IAudioEndpointVolume))
    volume_interface.SetMasterVolumeLevelScalar(volume, None)

def activate():
    print("Activating...")

    # take a picture of the intruder
    take_picture()
    
    # set volume to maximum (1.0)
    set_system_volume(1.0)

    # play an alert sound
    play_alert_sound("sound_effects/alert_sound.mp3")

    exit(0)


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
    toaster.show_toast(title, message, duration=10)

# main function
def main():

    # start the keyboard listener thread
    # keyboard_thread = threading.Thread(target=keyboard_listener)
    # keyboard_thread.start()

    print("Listening for key presses...")
    keyboard.on_press(on_key_press)
    keyboard.wait("esc") # execution will pause here until the "esc" key is pressed

if __name__ == "__main__":
    main()