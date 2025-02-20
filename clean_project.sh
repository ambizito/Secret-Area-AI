#!/bin/bash
echo "Removing __pycache__ directories..."
find . -type d -name "__pycache__" -exec rm -rf {} +
echo "Removing .pyc files..."
find . -type f -name "*.pyc" -delete
echo "Removing .pyo files..."
find . -type f -name "*.pyo" -delete
echo "Removing build artifacts..."
rm -rf build/ dist/ *.egg-info
echo "Cleanup complete."
