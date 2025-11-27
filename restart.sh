#!/bin/bash

echo "Stopping existing container..."
docker stop snacklore-test 2>/dev/null || true

echo "Removing old container..."
docker rm snacklore-test 2>/dev/null || true

echo "Rebuilding Docker image..."
docker build -t snacklore-app .

echo "Starting new container..."
docker run -d -p 5000:5000 --name snacklore-test snacklore-app

echo "Waiting for container to start..."
sleep 5

echo "Container logs:"
docker logs snacklore-test

echo ""
echo "Container is running!"
echo "Access the app at: http://localhost:5000"
echo "View logs with: docker logs -f snacklore-test"

