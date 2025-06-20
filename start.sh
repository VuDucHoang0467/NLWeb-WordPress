#!/bin/bash
echo "🚀 Starting NLWeb on Railway..."

# Create data directories
mkdir -p /app/data/db
mkdir -p /app/data/json
mkdir -p /app/data/json_with_embeddings

# Initialize Qdrant
echo "📦 Initializing Qdrant..."
python /app/init_qdrant.py

if [ $? -ne 0 ]; then
    echo "❌ Qdrant initialization failed"
    exit 1
fi

# Start the main application
echo "🎯 Starting NLWeb application..."
cd code
python app-file.py
