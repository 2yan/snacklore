#!/bin/bash

# Function to check if a port is in use
check_port() {
    lsof -i :5000 > /dev/null
    return $?
}

echo "Building Snacklore Docker image..."
docker build -t snacklore .

# Check if port 5000 is already in use
if check_port; then
    echo "Port 5000 is already in use. Attempting to stop existing container..."
    
    # Try to find container ID using port 5000 and stop it
    CONTAINER_ID=$(docker ps --filter "publish=5000" --format "{{.ID}}")
    
    if [ ! -z "$CONTAINER_ID" ]; then
        echo "Stopping Docker container $CONTAINER_ID..."
        docker stop $CONTAINER_ID
        echo "Container stopped."
    else
        echo "Could not identify Docker container on port 5000."
        echo "Please free up port 5000 manually."
        exit 1
    fi
fi

echo "Starting Snacklore container..."
docker run --rm -p 5000:5000 snacklore
