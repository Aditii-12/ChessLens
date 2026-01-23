import pyautogui
import time
import os

def capture_screen(save_dir="data/screenshots"):
    os.makedirs(save_dir, exist_ok=True)
    timestamp = int(time.time())
    path = f"{save_dir}/screenshot_{timestamp}.png"

    screenshot = pyautogui.screenshot()
    screenshot.save(path)

    return path
