#!/usr/bin/env python3  
  
import threading  
import time  
import subprocess  
import os  
from evdev import InputDevice, ecodes  
from pynput.mouse import Button, Controller as MouseController  
from pynput.keyboard import Controller as KeyboardController  
  
# Mouse device path  
DEVICE_PATH = "/dev/input/by-id/usb-Razer_Razer_DeathAdder_V3-event-mouse"  
  
# Button codes (from evdev)  
BUTTON_TURBO = 275      # Forward button  
BUTTON_PRESS_1 = 276    # Back button  
  
# Executable names of PoE (adjust if needed)  
POE_EXEC_NAMES = ["PathOfExile", "PathOfExileSteam"]  
  
mouse = MouseController()  
keyboard = KeyboardController()  
turbo_running = threading.Event()  
  
  
# Try to get active window PID via KWin DBus (Wayland)  
def get_active_window_pid():  
   try:  
       window_id = subprocess.check_output(  
           ["qdbus6", "org.kde.KWin", "/KWin", "org.kde.KWin.activeWindow"],  
           stderr=subprocess.DEVNULL,  
           text=True  
       ).strip()  
       if window_id:  
           pid = subprocess.check_output(  
               ["qdbus6", "org.kde.KWin", "/KWin", "org.kde.KWin.windowPid", window_id],  
               stderr=subprocess.DEVNULL,  
               text=True  
           ).strip()  
           return int(pid)  
   except Exception:  
       return None  
  
  
# Check if PoE is running in the active window or in the system processes  
def is_poe_active():  
   # First try KWin active window PID  
   pid = get_active_window_pid()  
   if pid:  
       try:  
           exe = os.readlink(f"/proc/{pid}/exe")  
           for name in POE_EXEC_NAMES:  
               if name.lower() in exe.lower():  
                   return True  
       except Exception:  
           pass  
  
   # Fallback: check system processes  
   try:  
       out = subprocess.check_output(["ps", "axo", "comm"], text=True)  
       processes = out.splitlines()  
       for name in POE_EXEC_NAMES:  
           if any(name.lower() in p.lower() for p in processes):  
               return True  
   except Exception:  
       pass  
  
   return False  
  
  
# Function to repeatedly click while turbo button is held  
def turbo_click():  
   while turbo_running.is_set():  
       if is_poe_active():  
           mouse.click(Button.left)  
           # Optional debug  
           # print("Turbo firing")  
           time.sleep(0.05)  # 20 clicks/sec  
       else:  
           time.sleep(0.2)  
  
  
# Listen to the mouse device  
def listen_device(path):  
   dev = InputDevice(path)  
   for event in dev.read_loop():  
       if event.type == ecodes.EV_KEY:  
           if event.code == BUTTON_TURBO:  
               if event.value == 1:  
                   turbo_running.set()  
                   threading.Thread(target=turbo_click, daemon=True).start()  
               elif event.value == 0:  
                   turbo_running.clear()  
           elif event.code == BUTTON_PRESS_1 and event.value == 1:  
               keyboard.press('1')  
               keyboard.release('1')  
  
  
if __name__ == "__main__":  
