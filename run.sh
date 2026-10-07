#!/bin/bash
# Navigate to project root directory (where this script is located)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment (.venv or venv)
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Error: Virtual environment (.venv or venv) not found in directory $SCRIPT_DIR"
    exit 1
fi

# Execute python script forwarding any arguments
python sfusion.py "$@"
