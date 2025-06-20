#!/usr/bin/env python3
"""
Export Qdrant local data for migration to cloud
"""

import os
import json
import asyncio
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

async def export_qdrant_data():
    """Export all data from local Qdrant to JSON"""
    
    # Connect to local Qdrant
    client = QdrantClient(path="../data/db")
    
    try:
        # Get collection info
        collections = client.get_collections()
        print(f"Found collections: {[col.name for col in collections.collections]}")
        
        for collection in collections.collections:
            collection_name = collection.name
            print(f"Exporting collection: {collection_name}")
            
            # Get all points
            points, _ = client.scroll(collection_name, limit=10000)
            
            # Export to JSON
            export_data = {
                "collection_name": collection_name,
                "points": [
                    {
                        "id": point.id,
                        "vector": point.vector,
                        "payload": point.payload
                    }
                    for point in points
                ]
            }
            
            # Save to file
            with open(f"../data/export_{collection_name}.json", "w") as f:
                json.dump(export_data, f, indent=2)
            
            print(f"Exported {len(points)} points from {collection_name}")
            
    except Exception as e:
        print(f"Error during export: {e}")
        return False
    
    return True

if __name__ == "__main__":
    asyncio.run(export_qdrant_data())
