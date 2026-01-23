import chess
from stockfish import Stockfish

# Update this path if needed (macOS homebrew default)
STOCKFISH_PATH = "/opt/homebrew/bin/stockfish"

stockfish = Stockfish(
    path=STOCKFISH_PATH,
    parameters={
        "Threads": 4,
        "Hash": 256
    }
)

def analyze_fen(fen, depth=3):
    """
    Takes a FEN string and returns top engine moves.
    """
    board = chess.Board(fen)
    stockfish.set_fen_position(fen)

    top_moves = stockfish.get_top_moves(depth)

    results = []
    for move in top_moves:
        cp = move.get("Centipawn")
        mate = move.get("Mate")

        if mate is not None:
            score = f"Mate in {mate}"
        elif cp is not None:
            score = f"{cp/100:.2f}"
        else:
            score = "?"

        results.append({
            "move": move["Move"],
            "score": score
        })

    return results
