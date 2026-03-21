import cv2
import mediapipe as mp
import numpy as np
import util
import pyautogui as pag
import time 
import json
import subprocess
import streamlit as st
def reset_data_files():
    """Clear JSON files at the start of each run."""
    json_files = [
        "data/chess_analysis.json",
        "data/latest_screen.json"
    ]

    for file in json_files:
        try:
            with open(file, "w") as f:
                json.dump({}, f)  # empty JSON object
            print(f"✅ Cleared {file}")
        except FileNotFoundError:
            # If file doesn't exist, create it empty
            with open(file, "w") as f:
                json.dump({}, f)
            print(f"✅ Created empty {file}")

screen_c=0
# Setup mediapipe
pag.FAILSAFE = False
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    model_complexity=1
)
draw = mp.solutions.drawing_utils

# Cooldown timers
last_left_click = 0
last_right_click = 0
last_screenshot = 0

# === New global for fist move detection ===
prev_wrist_y = None
fist_triggered = False


def move_mouse(index_finger_tip):
    if index_finger_tip is not None:
        x = int(index_finger_tip.x * pag.size().width)
        y = int(index_finger_tip.y * pag.size().height)
        pag.moveTo(x, y, duration=0.05)
    else:
        print("No finger tip detected")


def find_finger_tip(results):
    if results.multi_hand_landmarks:
        hand_landmark = results.multi_hand_landmarks[0]
        return hand_landmark.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
    return None


def is_left_click(landmark, thumb_index_distance, angle):
    return (
        angle < 50 and
        thumb_index_distance > 50 and
        util.get_angle(landmark[9], landmark[10], landmark[12]) > 90
    )


def is_right_click(landmark, thumb_index_distance, angle):
    return (
        angle > 90 and
        thumb_index_distance > 50 and
        util.get_angle(landmark[9], landmark[10], landmark[12]) < 50
    )


def palm_open_screenshot(land_mark):
    global last_screenshot
    global screen_c  # declare global separately

    thumb_pinky_dist = util.get_distance([land_mark[4], land_mark[20]])  # thumb tip = 4, pinky tip = 20

    # Check if thumb tip touches pinky tip (distance small enough)
    if thumb_pinky_dist is not None and thumb_pinky_dist < 40:  # adjust threshold as per your setup
        now = time.time()
        if now - last_screenshot > 4:  # Minimum 4 sec delay
            last_screenshot = now
            screen_c += 1   # increment counter
            print(f"Screenshot #{screen_c} taken")
            return True
    return False


# === New functions for fist + move down ===
def is_palm_closed(land_mark):
    """Check if most fingers are folded (fist)."""
    folded = 0
    for tip, base in [(8, 5), (12, 9), (16, 13), (20, 17)]:
        if land_mark[tip][1] > land_mark[base][1]:  # tip below base
            folded += 1
    return folded >= 3


def detect_fist_move_down(land_mark):
    global prev_wrist_y, fist_triggered
    wrist_y = land_mark[0][1]

    if prev_wrist_y is not None:
        delta_y = wrist_y - prev_wrist_y
        if delta_y > 20 and is_palm_closed(land_mark) and not fist_triggered:
            print("✊ Palm closed + move down → Switching window (⌘ + `)")
            pag.hotkey('command', '`')
            fist_triggered = True
            time.sleep(0.5)  # cooldown
        elif delta_y < -5:  # hand moved up → reset trigger
            fist_triggered = False

    prev_wrist_y = wrist_y


def detect_gesture(frame, land_mark, results):
    global last_left_click, last_right_click, last_screenshot
    global dragging, last_drag

    if len(land_mark) < 21:
        return

    index_finger_tip = find_finger_tip(results)
    thumb_index_dis = util.get_distance([land_mark[4], land_mark[5]])
    angle = util.get_angle(land_mark[5], land_mark[6], land_mark[8])

    if thumb_index_dis is not None:
        # Move mouse (pinch but not dragging)
        if thumb_index_dis < 50 and angle > 90:
            move_mouse(index_finger_tip)

        # Left click
        elif is_left_click(land_mark, thumb_index_dis, angle):
            if time.time() - last_left_click > 0.5:
                pag.click(button='left')
                print("Left Click")
                last_left_click = time.time()

        # Right click
        if is_right_click(land_mark, thumb_index_dis, angle):
            if time.time() - last_right_click > 0.5:
                pag.click(button='right')
                print("Right Click")
                last_right_click = time.time()

        if palm_open_screenshot(land_mark):
            print("Palm open detected → Running board.py")
            subprocess.Popen(["python3", "screen_shot.py"])
            pag.sleep(4)
            subprocess.Popen(["python3", "fen_gen.py"])
            with open("data/latest_screen.json", "w") as f:
                json.dump({"screen_c": screen_c}, f)

            # ✅ Create/Update flag file
            with open("data/ready.flag", "w") as f:
                f.write("ready")

            return True

    # === check fist move down ===
    detect_fist_move_down(land_mark)


def main():
    cap = cv2.VideoCapture(0)
    subprocess.Popen(
                ["venv/bin/streamlit", "run", "app.py"]
            )
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            h, w, c = frame.shape
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)
            land_mark = []

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    land_mark = np.array(
                        [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks.landmark]
                    )

            detect_gesture(frame, land_mark, results)
            cv2.imshow('ChessFlow', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    reset_data_files()
    main()