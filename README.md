# ♟️ ChessLens

ChessLens is a chess analysis project that integrates the **Stockfish chess engine** with a **Python-based application** to analyze chess positions and moves.  
The project focuses on building a strong foundation by combining classical chess engines with modern development tools, with plans to expand into a full-featured chess analysis system.

---

## 🚀 Project Status

**Current Phase:** Core Engine Integration (In Progress)

The project currently focuses on:
- Integrating Stockfish with Python
- Setting up a clean development environment
- Verifying engine execution locally
- Preparing the base structure for UI and analysis features

---

## 🧠 What Has Been Implemented

### Stockfish Engine
- Stockfish engine installed and verified locally
- Engine binary runs successfully from the terminal
- UCI protocol-based interaction confirmed

### Python Environment
- Virtual environment created for dependency isolation
- Required libraries installed
- Engine execution tested inside the virtual environment

### Project Structure
- Clean and organized directory layout
- Stockfish binary stored separately for easy upgrades
- Base application file created for future development

---

## 🛠️ Tech Stack

- **Language:** Python 3
- **Engine:** Stockfish (UCI)
- **Environment:** Python Virtual Environment (venv)
- **Platform:** macOS

---

## 📂 Project Structure

ChessLens/
├── bin/
│   └── stockfish
├── venv/
├── app.py
├── requirements.txt
└── README.md

---

## ▶️ How to Run the Project

### Clone the Repository
git clone <repository-url>  
cd ChessLens

### Activate Virtual Environment
source venv/bin/activate

### Test Stockfish Engine
./bin/stockfish

### Run the Application
python app.py

---

## 🎯 Planned Features

- Chessboard UI using Streamlit
- Position evaluation and best-move suggestions
- Move-by-move analysis
- Game review (blunders, mistakes, best moves)
- PGN file upload and analysis
- (Future) Machine learning-based player insights

---

## 💡 Learning Outcomes

- Chess engines and the UCI protocol
- Python system-level integration
- Virtual environments and dependency management
- Debugging engine-driven applications
- Structuring scalable software projects

---

## 🤝 Contributions

This project is under active development.  
Suggestions, issues, and contributions are welcome.

---

## 📌 Note

This README reflects the **current progress** of the project.  
Features and structure will evolve as development continues.

---

Built with Python, Stockfish, and curiosity.
