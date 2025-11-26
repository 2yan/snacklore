# Flask Hello World

A simple Flask application.

## Setup

### Using Docker (Recommended)

1.  Build the Docker image:
    ```bash
    docker build -t flask-hello-world .
    ```

2.  Run the container:
    ```bash
    docker run -p 5000:5000 flask-hello-world
    ```

3.  Open http://127.0.0.1:5000 in your browser.

### Local Development

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2.  Run the application:
    ```bash
    python app.py
    ```

3.  Open http://127.0.0.1:5000 in your browser.

