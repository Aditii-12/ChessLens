import pyautogui
import os
import json

# ✅ FIX 1: Ensure required directories exist
save_dir = "assets/moves"
os.makedirs(save_dir, exist_ok=True)
os.makedirs("data", exist_ok=True)

# Find the next available screenshot number
existing = [
    int(f.split(".")[0])
    for f in os.listdir(save_dir)
    if f.split(".")[0].isdigit()
]
next_num = max(existing) + 1 if existing else 1

save_path = os.path.join(save_dir, f"{next_num}.png")

pyautogui.sleep(1)

# Adjust this region to match the chess.com board on your screen
# region = (left, top, width, height)
board_region = (319, 147, 560, 560)
board_image = pyautogui.screenshot(region=board_region)
board_image.save(save_path)
print(f"✅ Screenshot saved at: {save_path}")

# ✅ FIX 2: Write latest_screen.json here (original file never did this)
#           fen_gen.py reads this to know which image to process.
#           Without this, fen_gen.py crashes immediately on every run.
with open("data/latest_screen.json", "w") as f:
    json.dump({"screen_c": next_num}, f)
print(f"✅ latest_screen.json updated → screen_c={next_num}")