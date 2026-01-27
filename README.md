# ♟️ ChessLens

ChessLens is a Python-based chess analysis and automation project that captures live chessboard states from the screen, converts them into FEN notation, and analyzes positions using the Stockfish chess engine.  
It also includes mouse automation and structured runtime data handling for a smooth analysis pipeline.

---

## ✨ Features

- Screenshot-based chessboard capture  
- FEN generation from captured board state  
- Stockfish-powered position analysis  
- Mouse automation using PyAutoGUI  
- Runtime data management using JSON and flags  
- SQLite database support for structured storage  

---

## 🛠️ Tech Stack

- Python 3  
- Stockfish (UCI chess engine)  
- python-chess  
- OpenCV  
- PyAutoGUI  
- SQLite  
- Virtual Environment (venv)

---

## 📂 Project Structure

ChessLens/
├── assets/                Static assets  
├── data/                  Runtime-generated files  
│   ├── chess_analysis.json  
│   ├── latest_screen.json  
│   └── ready.flag  
├── app.py                 Main entry point  
├── runner.py              Controls execution flow  
├── mouse.py               Mouse automation logic  
├── screen_shot.py         Screenshot capture  
├── fen_gen.py             FEN generation logic  
├── database.py            SQLite handling  
├── util.py                Helper utilities  
├── requirements.txt  
├── .gitignore  
└── README.md  

---

## 🎯 Use Cases

- Automated chess position analysis  
- Studying best moves and evaluations  
- Assisting real-time chess gameplay  
- Extending chess tooling on top of Stockfish  

---

## 🚀 Clone & Setup

Clone the repository  
git clone https://github.com/aditi-12/ChessLens.git  
cd ChessLens  

Create virtual environment (Python 3.11 recommended)  
python3.11 -m venv venv  

Activate virtual environment  
source venv/bin/activate        (macOS / Linux)  
venv\\Scripts\\activate         (Windows)  

Install dependencies  
pip install -r requirements.txt  

---

## ▶️ Running the Project

Run the main application  
python app.py  

The program will:
- Capture the chessboard from screen  
- Generate FEN using image processing  
- Analyze the position with Stockfish  
- Store results inside the data directory  

---

## 📌 Notes

ChessLens is a backend-focused project built for automation and analysis.  
The architecture allows easy extension into UI or advanced analytics in the future.

---

Built with Python, Stockfish, and persistence.
