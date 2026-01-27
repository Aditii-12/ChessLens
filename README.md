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

```text
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
```
---

## 🎯 Use Cases

- Automated chess position analysis  
- Studying best moves and engine evaluations  
- Assisting real-time chess gameplay  
- Extending custom chess tooling on top of Stockfish  
---

## 🚀 Clone & Setup

```bash
git clone https://github.com/Aditii-12/ChessLens.git
cd ChessLens
```
```bash
python3.11 -m venv venv
source venv/bin/activate
venv\Scripts\activate  (Windows)
```
```bash

pip install -r requirements.txt
```
---

## ▶️ Running the Project
```bash
python app.py
```


The program will:
- Capture the chessboard from the screen
- Generate FEN using image processing
- Analyze the position with Stockfish
- Store results inside the data directory

---

## 📌 Notes

- Designed for backend-driven chess analysis and automation  
- Requires a visible chessboard on screen for accurate capture  
- Structured to allow future UI or analytics extensions

---

## 👤 Author

Aditi Sahu
