from selenium import webdriver
from selenium.webdriver.common.by import By
import os, time, json
import chess
from stockfish import Stockfish

# Path to your image (screenshot of chessboard)
import json

# read latest screenshot counter
with open("data/latest_screen.json", "r") as f:
    data = json.load(f)
    screen_c = data["screen_c"]

# now build path dynamically
IMAGE_PATH = f"assets/moves/{screen_c}.png"

# Path to Brave browser binary (adjust if installed somewhere else)
brave_path = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"

# Configure ChromeOptions for Brave
options = webdriver.ChromeOptions()
options.binary_location = brave_path
options.add_argument("--headless")   # Run browser in background (no window)

# Start Chrome WebDriver (Brave)
driver = webdriver.Chrome(options=options)

# Open the OCR website
driver.get("https://helpman.komtera.lt/chessocr/")

# Upload the image file into OCR input
upload = driver.find_element(By.CSS_SELECTOR, "input[type=file]")
upload.send_keys(os.path.abspath(IMAGE_PATH))

# Wait for OCR processing
time.sleep(3)  # Increase if internet/processing is slow

# Extract detected FEN string from website
fen_box = driver.find_element(By.CSS_SELECTOR, "input[type=text]")
fen = fen_box.get_attribute("value")

# Close browser
driver.quit()

# --- Prepare FENs for both sides ---
fen_full = fen + " w - - 0 1"         # Assume White to move
flipped_fen_full = fen + " b - - 0 1"  # Assume Black to move

# --- Initialize Stockfish engine ---
stockfish = Stockfish(path="/opt/homebrew/bin/stockfish")
stockfish.update_engine_parameters({
    "Threads": 4,          
    "Hash": 512,           
    "UCI_LimitStrength": False  
})

# --- Function: Get top 3 best moves for current position ---
def get_top_moves(stockfish, fen):
    board = chess.Board(fen)
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
        results.append({
            "move": move['Move'],
            "score": score
        })
    return results

# --- Function: Predict future moves ---
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

# --- Collect results ---
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

# --- Save to JSON file ---
OUTPUT_FILE = "data/chess_analysis.json"
with open(OUTPUT_FILE, "w") as f:
    json.dump(results, f, indent=4)

print(f"✅ Results saved to {OUTPUT_FILE}")