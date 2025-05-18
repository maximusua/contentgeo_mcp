#!/bin/bash

# Build and run the ContentGeo MCP server

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Build and start the container
echo "Building and starting ContentGeo MCP server..."
docker compose up --build -d

# Wait for the container to start
echo "Waiting for server to start..."
sleep 5

# Check if the server is running
if docker compose ps | grep -q "Up"; then
    echo "ContentGeo MCP server is running!"
    echo "Server available at: http://localhost:8000"
    echo "Test health endpoint at: http://localhost:8000/health_check"
else
    echo "Failed to start ContentGeo MCP server. Check logs with: docker compose logs"
    exit 1
fi 