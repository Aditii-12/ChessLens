import os
import sys
import time
import json

import chess
from stockfish import Stockfish
from selenium import webdriver
from selenium.webdriver.common.by import By

# ✅ FIX 1: Ensure data directory exists
os.makedirs("data", exist_ok=True)

# ✅ FIX 2: Guard against missing latest_screen.json (crash on first run)
if not os.path.exists("data/latest_screen.json"):
    print("❌ data/latest_screen.json not found. Run screen_shot.py first.")
    sys.exit(1)

with open("data/latest_screen.json", "r") as f:
    data = json.load(f)

screen_c = data.get("screen_c")
if not screen_c:
    print("❌ 'screen_c' key missing in latest_screen.json.")
    sys.exit(1)

IMAGE_PATH = f"assets/moves/{screen_c}.png"

# ✅ FIX 3: Guard against missing screenshot file
if not os.path.exists(IMAGE_PATH):
    print(f"❌ Screenshot not found at {IMAGE_PATH}. Run screen_shot.py first.")
    sys.exit(1)

# Mac: Brave browser path (you said you'll update this later — left as-is)
BRAVE_PATH = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"

options = webdriver.ChromeOptions()
options.binary_location = BRAVE_PATH
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

try:
    driver.get("https://helpman.komtera.lt/chessocr/")

    upload = driver.find_element(By.CSS_SELECTOR, "input[type=file]")
    upload.send_keys(os.path.abspath(IMAGE_PATH))

    time.sleep(3)

    fen_box = driver.find_element(By.CSS_SELECTOR, "input[type=text]")
    fen = fen_box.get_attribute("value")
finally:
    driver.quit()

# ✅ FIX 4: Guard against empty FEN from OCR
if not fen or not fen.strip():
    print("❌ FEN extraction failed — OCR returned empty result.")
    sys.exit(1)

print(f"✅ FEN extracted: {fen}")

fen_full = fen + " w - - 0 1"
flipped_fen_full = fen + " b - - 0 1"

# Mac: Stockfish path via Homebrew (you said you'll update this — left as-is)
STOCKFISH_PATH = "/opt/homebrew/bin/stockfish"

# ✅ FIX 5: Removed duplicate `import json` that was in original file
stockfish = Stockfish(path=STOCKFISH_PATH)
stockfish.update_engine_parameters({
    "Threads": 4,
    "Hash": 512,
    "UCI_LimitStrength": False
})

def get_top_moves(stockfish, fen):
    stockfish.set_fen_position(fen)
    top_moves = stockfish.get_top_moves(3)
    results = []
    for move in top_moves:
        cp = move.get("Centipawn")
        mate = move.get("Mate")
        if mate is not None:
            score = f"Mate in {mate}"
        else:
            score = f"Eval: {cp/100:.2f}" if cp is not None else "?"
        results.append({"move": move['Move'], "score": score})
    return results

def predict_future_moves(stockfish, fen, depth=10):
    stockfish.set_fen_position(fen)
    moves_sequence = []
    for _ in range(depth):
        best_move = stockfish.get_best_move()
        if not best_move:
            break
        moves_sequence.append(best_move)
        stockfish.make_moves_from_current_position([best_move])
    return moves_sequence

results = {
    "Current_FEN": {
        "fen": fen_full,
        "best_moves": get_top_moves(stockfish, fen_full),
        "future_moves": predict_future_moves(stockfish, fen_full, depth=10)
    },
    "Flipped_FEN": {
        "fen": flipped_fen_full,
        "best_moves": get_top_moves(stockfish, flipped_fen_full),
        "future_moves": predict_future_moves(stockfish, flipped_fen_full, depth=10)
    }
}

OUTPUT_FILE = "data/chess_analysis.json"
with open(OUTPUT_FILE, "w") as f:
    json.dump(results, f, indent=4)
print(f"✅ Results saved to {OUTPUT_FILE}")

# ✅ FIX 6: Write ready.flag — without this app.py NEVER shows results
with open("data/ready.flag", "w") as f:
    f.write("ready")
print("✅ ready.flag written — dashboard will now display results.")