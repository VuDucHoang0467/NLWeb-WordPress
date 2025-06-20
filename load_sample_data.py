#!/usr/bin/env python3
"""
Load sample data into Qdrant for testing
This script adds some sample documents to test the system
"""

import os
import sys
import asyncio
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'code'))

from embedding.embedding import get_embedding

async def load_sample_data():
    """Load sample data into Qdrant collection"""
    
    collection_name = "nlweb_collection"
    data_dir = "/app/data/db"
    
    # Sample documents
    sample_docs = [
        {
            "id": 1,
            "text": "Welcome to NLWeb - an intelligent web search and chat system",
            "name": "NLWeb Introduction",
            "url": "https://github.com/microsoft/nlweb",
            "description": "Introduction to NLWeb system"
        },
        {
            "id": 2, 
            "text": "NLWeb uses OpenAI embeddings and Qdrant vector database for semantic search",
            "name": "NLWeb Technology",
            "url": "https://github.com/microsoft/nlweb/docs",
            "description": "Technology stack used in NLWeb"
        },
        {
            "id": 3,
            "text": "You can deploy NLWeb on Railway, Render, or any cloud platform with Docker support",
            "name": "NLWeb Deployment",
            "url": "https://github.com/microsoft/nlweb/deployment", 
            "description": "How to deploy NLWeb to cloud platforms"
        }
    ]
    
    try:
        # Initialize Qdrant client
        client = QdrantClient(path=data_dir)
        
        # Check if collection has data
        info = client.get_collection(collection_name)
        if info.points_count > 0:
            print(f"✅ Collection already has {info.points_count} points, skipping sample data")
            return True
            
        print("📝 Loading sample data...")
        
        # Generate embeddings and upload points
        points = []
        for doc in sample_docs:
            print(f"🔤 Generating embedding for: {doc['name']}")
            
            # Get embedding
            embedding = await get_embedding(doc['text'])
            if embedding is None:
                print(f"❌ Failed to generate embedding for: {doc['name']}")
                continue
                
            # Create point
            point = PointStruct(
                id=doc['id'],
                vector=embedding,
                payload={
                    "name": doc['name'],
                    "url": doc['url'], 
                    "description": doc['description'],
                    "text": doc['text'],
                    "site": "sample"
                }
            )
            points.append(point)
        
        # Upload points
        if points:
            client.upsert(collection_name=collection_name, points=points)
            print(f"✅ Uploaded {len(points)} sample documents")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading sample data: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(load_sample_data())
    if success:
        print("🎉 Sample data loaded successfully!")
    else:
        print("⚠️ Sample data loading failed, but system can still work")
        # Don't exit with error - system can work without sample data
