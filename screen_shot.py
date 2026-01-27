import pyautogui
import os

# Ensure the folder exists
save_dir = "assets/moves"
os.makedirs(save_dir, exist_ok=True)

# Find the next available number
existing = [int(f.split(".")[0]) for f in os.listdir(save_dir) if f.split(".")[0].isdigit()]
next_num = max(existing) + 1 if existing else 1

# File path
save_path = os.path.join(save_dir, f"{next_num}.png")

# Adjust the region to match the chess.com board on your screen
# region = (left, top, width, height)
pyautogui.sleep(1)

board_region = (319, 147, 560, 560)
board_image = pyautogui.screenshot(region=board_region)
board_image.save(save_path)

print(f"Screenshot saved at: {save_path}")