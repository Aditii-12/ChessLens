import cv2
import mediapipe as mp
import numpy as np
import util
import pyautogui as pag
import time
import json
import subprocess

pag.FAILSAFE = False
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
draw = mp.solutions.drawing_utils

screen_c = 0
last_shot = 0

def main():
    global last_shot, screen_c
    cap = cv2.VideoCapture(0)
    subprocess.Popen(["streamlit", "run", "app.py"])

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = hands.process(rgb)

        if res.multi_hand_landmarks:
            lm = res.multi_hand_landmarks[0]
            draw.draw_landmarks(frame, lm, mp_hands.HAND_CONNECTIONS)
            pts = np.array([(int(p.x*frame.shape[1]), int(p.y*frame.shape[0])) for p in lm.landmark])

            if util.get_distance([pts[4], pts[20]]) < 40:
                if time.time() - last_shot > 4:
                    last_shot = time.time()
                    screen_c += 1

                    with open("data/latest_screen.json", "w") as f:
                        json.dump({"screen_c": screen_c}, f)

                    subprocess.Popen(["python3", "screen_shot.py"])
                    time.sleep(3)
                    subprocess.Popen(["python3", "fen_gen.py"])

        cv2.imshow("ChessLens", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

main()
