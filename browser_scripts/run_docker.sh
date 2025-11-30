#!/bin/bash

# Script to run browser scripts in Docker

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

# Build the Docker image
echo "Building Docker image for browser scripts..."
docker build -f browser_scripts/Dockerfile -t browser-scripts .

# Run the script with provided arguments
if [ "$#" -eq 0 ]; then
    echo "Usage: ./run_docker.sh <script_name> [arguments...]"
    echo "Example: ./run_docker.sh find_national_dishes.py India"
    echo "Example: ./run_docker.sh get_cooking_instructions.py 'Chicken Tikka Masala' India"
    exit 1
fi

SCRIPT_NAME="$1"
shift

echo "Running $SCRIPT_NAME with arguments: $@"
docker run -it --rm \
    -e OPENAI_API_KEY="${OPENAI_API_KEY}" \
    -v "$(pwd)/browser_scripts:/app" \
    browser-scripts \
    python3 "$SCRIPT_NAME" "$@"


