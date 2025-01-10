#!/bin/bash

# Exit on any error
set -e

echo "Copying frontend build to backend..."
rm -rf ./gym-attendance-backend/static # Clean up old static files
cp -r ./gym-attendance-frontend/build ./gym-attendance-backend/static # Copy new frontend build

echo "Frontend build is copied to backend."

echo "$AWS_PRIVATE_KEY" > aws_private_key.pem
echo "$AWS_CERT" > aws_cert.pem
echo "$AWS_CA_CERT" > aws_ca_cert.pem

cat aws_private_key.pem
cat aws_cert.pem
cat aws_ca_cert.pem

echo "Certificates are created."

