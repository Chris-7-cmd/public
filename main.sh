#!/bin/bash

# Run the static site generator
echo "Generating static site..."
python3 src/main.py

# Start a simple HTTP server in the public directory
echo "Starting HTTP server on port 8888..."
cd docs && python3 -m http.server 8888

echo "Server stopped."