from stockfish import Stockfish
import chess, json

stockfish = Stockfish("/opt/homebrew/bin/stockfish")

def analyze(fen):
    stockfish.set_fen_position(fen)
    return stockfish.get_top_moves(3)

fen = chess.STARTING_FEN
data = {
    "Current_FEN":{
        "best_moves": analyze(fen),
        "future_moves": [stockfish.get_best_move()]
    }
}
json.dump(data, open("data/chess_analysis.json","w"), indent=4)
