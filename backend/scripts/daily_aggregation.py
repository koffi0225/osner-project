#!/usr/bin/env python3
"""
Script de mise à jour automatique quotidienne
Exécute l'agrégation de tout le contenu (emplois, actualités, formations)
"""

import asyncio
import aiohttp
import sys
import os
from datetime import datetime

# URL de l'API
API_URL = os.environ.get('REACT_APP_BACKEND_URL', 'http://localhost:8001')
AGGREGATION_ENDPOINT = f"{API_URL}/api/aggregation/update-all"

async def run_aggregation():
    print(f"[{datetime.now()}] Starting daily content aggregation...")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(AGGREGATION_ENDPOINT, timeout=300) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"[{datetime.now()}] Aggregation successful!")
                    print(f"Results: {result}")
                    return 0
                else:
                    error_text = await response.text()
                    print(f"[{datetime.now()}] Aggregation failed with status {response.status}")
                    print(f"Error: {error_text}")
                    return 1
    except Exception as e:
        print(f"[{datetime.now()}] Error during aggregation: {str(e)}")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(run_aggregation())
    sys.exit(exit_code)