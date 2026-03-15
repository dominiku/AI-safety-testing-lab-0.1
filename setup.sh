#!/usr/bin/env bash
# setup.sh - Environment Setup for AI Safety Lab 02

set -e

echo "==========================================="
echo "   AI Safety Lab 02 - Environment Setup    "
echo "==========================================="

# 1. Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH."
    exit 1
fi
echo "✅ Python 3 found."

# 2. Create virtual environment
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment (.venv)..."
    python3 -m venv .venv
else
    echo "👍 Virtual environment (.venv) already exists."
fi

# 3. Activate and install requirements
echo "⚙️  Installing dependencies..."
source .venv/bin/activate
pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "❌ requirements.txt not found!"
    exit 1
fi
echo "✅ Dependencies installed successfully."

# 4. Create .env file template if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file template..."
    cat <<EOF > .env
# Configuration for AI Safety Lab 02
CF_ACCESS_CLIENT_ID=your_client_id_here
CF_ACCESS_CLIENT_SECRET=your_client_secret_here
EOF
    echo "⚠️  Please update the .env file with your actual Cloudflare Access credentials!"
else
    echo "👍 .env file already exists."
fi

# 5. Ensure required directories exist
mkdir -p logs prompts suites

echo "==========================================="
echo "✅ Setup Complete!"
echo "To activate your environment and run tests, use:"
echo ""
echo "    source .venv/bin/activate"
echo "    python run_suite.py"
echo "==========================================="
