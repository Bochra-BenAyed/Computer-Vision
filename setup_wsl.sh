#!/usr/bin/env bash
# One-shot setup for Ubuntu on WSL2. Run from the repo root:  bash setup_wsl.sh
set -e

echo "==> 1/4 Installing system packages (asks for your sudo password)"
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git ffmpeg \
    libgl1 libglib2.0-0 postgresql postgresql-contrib

echo "==> 2/4 Creating the Python virtual environment in .venv"
python3 -m venv .venv

echo "==> 3/4 Installing Python dependencies (PyTorch is large, this can take several minutes)"
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

echo "==> 4/4 Checking the install"
.venv/bin/python - <<'EOF'
import cv2, torch, ultralytics
print("OpenCV      :", cv2.__version__)
print("PyTorch     :", torch.__version__)
print("GPU visible :", torch.cuda.is_available(), "(False is fine, CPU works)")
print("Ultralytics :", ultralytics.__version__)
EOF

echo
echo "Done. Activate the environment with:  source .venv/bin/activate"
