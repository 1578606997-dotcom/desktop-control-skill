#!/bin/bash
# Desktop Control Skill Installer
# Installs Python dependencies for Windows desktop automation

echo "🖥️  Installing Desktop Control Skill..."

# Check Python
python --version > /dev/null 2>&1 || python3 --version > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Python not found. Please install Python 3.8+"
    exit 1
fi

# Check Windows (this skill is Windows-only)
if [[ "$OSTYPE" != "msys" && "$OSTYPE" != "cygwin" && "$OSTYPE" != "win32" ]]; then
    echo "⚠️  Warning: This skill is designed for Windows"
    echo "   Current OS: $OSTYPE"
fi

echo "📦 Installing Python packages..."
pip install -q pyautogui mss pillow opencv-python numpy

if [ $? -eq 0 ]; then
    echo "✅ Desktop Control Skill installed successfully!"
    echo ""
    echo "Usage examples:"
    echo "  openclaw skills run desktop-control screen_size"
    echo "  openclaw skills run desktop-control mouse_pos"
    echo "  openclaw skills run desktop-control screenshot --full"
    echo "  openclaw skills run desktop-control click --x 500 --y 300"
else
    echo "❌ Installation failed"
    exit 1
fi
