import subprocess
import sys
import time

# ✅ FIX 1: Open chess.com in Brave on Mac
print("🌐 Opening chess.com in Brave...")
subprocess.Popen(["open", "-na", "Brave Browser", "--args", "https://www.chess.com"])

# ✅ FIX 2: Wait for the browser + game to load before screenshotting
print("⏳ Waiting for game to load (15 seconds)...")
time.sleep(15)

# ✅ FIX 3: Original runner.py NEVER ran screen_shot.py or fen_gen.py
#           so clicking Play produced zero analysis. Now the full pipeline runs.
print("📸 Taking screenshot...")
result = subprocess.run([sys.executable, "screen_shot.py"])
if result.returncode != 0:
    print("❌ screen_shot.py failed. Aborting.")
    sys.exit(1)

print("🧠 Running Stockfish analysis...")
result = subprocess.run([sys.executable, "fen_gen.py"])
if result.returncode != 0:
    print("❌ fen_gen.py failed. Aborting.")
    sys.exit(1)

print("✅ Pipeline complete — check the dashboard for results.")