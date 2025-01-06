#!/bin/bash

# Exit on any error
set -e

echo "Copying frontend build to backend..."
rm -rf ./gym-attendance-backend/static # Clean up old static files
cp -r ./gym-attendance-frontend/build ./gym-attendance-backend/static # Copy new frontend build

echo "Frontend build is copied to backend."
