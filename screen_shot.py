import pyautogui
import os
import time

def capture_screen(save_dir="data/screenshots"):
    os.makedirs(save_dir, exist_ok=True)
    timestamp = int(time.time())
    path = os.path.join(save_dir, f"screenshot_{timestamp}.png")

    img = pyautogui.screenshot()
    img.save(path)

    return path
