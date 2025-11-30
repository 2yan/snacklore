# Browser Scripts

This folder contains browser-use based scripts for finding national dishes and cooking instructions.

## Scripts

### 1. find_national_dishes.py

Finds the national dish(es) of a given country using Wikipedia.

### 2. get_cooking_instructions.py

Gets detailed cooking instructions for a dish from a specific country by searching online.

## Running with Docker (Recommended)

The easiest way to run these scripts is using Docker, which handles all dependencies automatically.

### Quick Start

```bash
# Make sure you have OPENAI_API_KEY set in your environment
export OPENAI_API_KEY="your-api-key-here"

# Run the script to find national dishes
./browser_scripts/run_docker.sh find_national_dishes.py India

# Run the script to get cooking instructions
./browser_scripts/run_docker.sh get_cooking_instructions.py "Chicken Tikka Masala" India
```

### Manual Docker Commands

If you prefer to use Docker commands directly:

```bash
# Build the image
docker build -f browser_scripts/Dockerfile -t browser-scripts .

# Run find_national_dishes.py
docker run -it --rm \
    -e OPENAI_API_KEY="${OPENAI_API_KEY}" \
    -v "$(pwd)/browser_scripts:/app" \
    browser-scripts \
    python3 find_national_dishes.py India

# Run get_cooking_instructions.py
docker run -it --rm \
    -e OPENAI_API_KEY="${OPENAI_API_KEY}" \
    -v "$(pwd)/browser_scripts:/app" \
    browser-scripts \
    python3 get_cooking_instructions.py "Chicken Tikka Masala" India
```

## Local Installation (Alternative)

If you prefer to run locally without Docker:

```bash
pip install -r browser_scripts/requirements.txt
playwright install chromium
playwright install-deps chromium
```

Then run:
```bash
python3 browser_scripts/find_national_dishes.py India
python3 browser_scripts/get_cooking_instructions.py "Chicken Tikka Masala" India
```

## Requirements

- Docker (for Docker method) OR Python 3.11+ (for local method)
- OpenAI API key (set as `OPENAI_API_KEY` environment variable)
- Internet connection

## Notes

- The scripts use browser automation with AI agents in headless mode
- The scripts use AI agents to navigate and extract information from websites intelligently
- Make sure you have a stable internet connection when running these scripts
- The scripts may take some time to complete as they navigate websites and extract information
- You need to set up an OpenAI API key for the LLM used by browser-use

