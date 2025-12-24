#!/bin/bash

# LinkForge Cleanup Script
# Removes all auto-generated files, caches, and build artifacts.

echo "🧹 Cleaning up LinkForge project..."

# Remove Python cache directories
echo "Removing __pycache__..."
find . -type d -name "__pycache__" -exec rm -rf {} +

# Remove tool caches
echo "Removing tool caches (.mypy_cache, .pytest_cache, .ruff_cache)..."
rm -rf .mypy_cache .pytest_cache .ruff_cache

# Remove build artifacts
echo "Removing build artifacts (dist, build, egg-info)..."
rm -rf dist build *.egg-info

# Remove coverage reports
echo "Removing coverage reports..."
rm -rf htmlcov .coverage coverage.xml coverage.json

# Remove virtual environments
echo "Removing virtual environments (.venv, venv)..."
rm -rf .venv venv

echo "✨ Cleanup complete! Project is clean."
