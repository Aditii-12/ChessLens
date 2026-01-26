from stockfish import Stockfish

STOCKFISH_PATH = "bin/stockfish"

stockfish = Stockfish(
    path=STOCKFISH_PATH,
    parameters={
        "Threads": 2,
        "Minimum Thinking Time": 30
    }
)

def analyze_fen(fen):
    stockfish.set_fen_position(fen)
    top_moves = stockfish.get_top_moves(3)

    results = []
    for move in top_moves:
        score = move.get("Centipawn")
        mate = move.get("Mate")

        if mate is not None:
            eval_score = f"Mate in {mate}"
        else:
            eval_score = f"{score/100:.2f}" if score else "?"

        results.append({
            "move": move["Move"],
            "score": eval_score
        })

    return results
