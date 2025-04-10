#!/bin/bash

# Get the repository name
REPO_NAME=$(basename -s .git `git config --get remote.origin.url`)

# Run the static site generator with the repository name as the base path
python3 src/main.py "/$REPO_NAME/"

echo "Site built successfully with base path: /$REPO_NAME/"
echo "The site is available in the 'docs' directory"