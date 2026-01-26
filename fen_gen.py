from stockfish import Stockfish
import chess
import json
import os

# ✅ Correct Stockfish binary path for Mac (Homebrew)
STOCKFISH_PATH = "/opt/homebrew/bin/stockfish"

stockfish = Stockfish(path=STOCKFISH_PATH)
stockfish.update_engine_parameters({
    "Threads": 2,
    "Hash": 128
})

def get_top_moves(fen, n=3):
    stockfish.set_fen_position(fen)
    moves = stockfish.get_top_moves(n)

    results = []
    for m in moves:
        cp = m.get("Centipawn")
        mate = m.get("Mate")
        if mate is not None:
            score = f"Mate {mate}"
        elif cp is not None:
            score = f"{cp/100:.2f}"
        else:
            score = "?"
        results.append({
            "move": m["Move"],
            "score": score
        })
    return results

def predict_future_moves(fen, depth=5):
    stockfish.set_fen_position(fen)
    seq = []
    for _ in range(depth):
        move = stockfish.get_best_move()
        if not move:
            break
        seq.append(move)
        stockfish.make_moves_from_current_position([move])
    return seq

# For now: assume starting position
fen = chess.STARTING_FEN

results = {
    "Current_FEN": {
        "fen": fen,
        "best_moves": get_top_moves(fen),
        "future_moves": predict_future_moves(fen)
    }
}

os.makedirs("data", exist_ok=True)
with open("data/chess_analysis.json", "w") as f:
    json.dump(results, f, indent=4)

# Signal Streamlit that analysis is ready
with open("data/ready.flag", "w") as f:
    f.write("ready")
