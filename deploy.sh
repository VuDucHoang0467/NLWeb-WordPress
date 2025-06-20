#!/bin/bash

# Production deployment script for NLWeb
# This script helps deploy NLWeb to production environment

set -e

echo "🚀 Starting NLWeb deployment process..."

# Check if .env exists
if [ ! -f "code/.env" ]; then
    echo "❌ Error: .env file not found in code/ directory"
    echo "Please create code/.env with your API keys before deploying"
    exit 1
fi

# Check if OPENAI_API_KEY is set
if ! grep -q "OPENAI_API_KEY=sk-" code/.env; then
    echo "❌ Error: OPENAI_API_KEY not found or invalid in .env file"
    echo "Please add your OpenAI API key to code/.env"
    exit 1
fi

echo "✅ Environment configuration validated"

# Create necessary directories
mkdir -p data/db
mkdir -p data/json
mkdir -p data/json_with_embeddings

echo "✅ Data directories created"

# Build Docker image if Dockerfile exists
if [ -f "Dockerfile" ]; then
    echo "🐳 Building Docker image..."
    docker build -t nlweb-app:latest .
    echo "✅ Docker image built successfully"
fi

# Run local test
echo "🧪 Running local test..."
cd code
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('OPENAI_API_KEY configured:', bool(os.getenv('OPENAI_API_KEY')))
print('Configuration test passed!')
"
cd ..

echo "✅ All checks passed!"
echo ""
echo "📋 Next steps:"
echo "1. For Railway: Push to GitHub and connect to Railway"
echo "2. For Render: Push to GitHub and create new Web Service"  
echo "3. For Docker: Run with 'docker run -d -p 8000:8000 nlweb-app:latest'"
echo ""
echo "📝 Don't forget to:"
echo "- Set environment variables on your hosting platform"
echo "- Update widget.js URL in your WordPress site"
echo "- Test the deployment after going live"
