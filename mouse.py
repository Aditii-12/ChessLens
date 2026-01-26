import cv2, mediapipe as mp, numpy as np, pyautogui as pag
import util, time, json, subprocess

pag.FAILSAFE = False
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
draw = mp.solutions.drawing_utils
screen_c = 0

def main():
    cap = cv2.VideoCapture(0)
    subprocess.Popen(["streamlit", "run", "app.py"])
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame,1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = hands.process(rgb)

        if res.multi_hand_landmarks:
            lm = res.multi_hand_landmarks[0]
            draw.draw_landmarks(frame, lm, mp_hands.HAND_CONNECTIONS)
            pts = np.array([(int(p.x*frame.shape[1]),int(p.y*frame.shape[0])) for p in lm.landmark])
            if util.get_distance([pts[4],pts[20]]) < 40:
                screen_c += 1
                subprocess.Popen(["python3","screen_shot.py"])
                time.sleep(2)
                subprocess.Popen(["python3","fen_gen.py"])
                with open("data/latest_screen.json","w") as f:
                    json.dump({"screen_c":screen_c},f)
                open("data/ready.flag","w").write("ready")

        cv2.imshow("ChessLens",frame)
        if cv2.waitKey(1)&0xFF==ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

main()
