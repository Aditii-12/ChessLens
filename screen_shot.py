import pyautogui, os
os.makedirs("assets/moves",exist_ok=True)
img = pyautogui.screenshot(region=(319,147,560,560))
img.save("assets/moves/1.png")
