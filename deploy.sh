#!/bin/bash

# Exit on any error
set -e

echo "Building frontend..."
cd gym-attendance-frontend # Navigate to the frontend directory
npm install # Install dependencies (if needed)
npm run build # Build the React app

echo "Copying frontend build to backend..."
cd ..
rm -rf ./gym-attendance-backend/static # Clean up old static files
cp -r ./gym-attendance-frontend/build ./gym-attendance-backend/static

echo "Frontend build is complete and copied to backend."
