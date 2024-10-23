# run_rufus.py

import sys

# For Windows systems, adjust the event loop policy
import asyncio

if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Set stdout encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

from rufus import RufusClient, RufusConfig

config = RufusConfig(
    max_depth=10,  # Increase depth for deeper crawling
    extraction_granularity='paragraph',
    evaluation_threshold=0.5,
    relevance_threshold=0.2,  # Lower threshold to include more pages
    max_pages=1000,  # Increase max pages to crawl more content
    concurrency=20,  # Increase concurrency if needed
)

client = RufusClient(config=config)

url = "https://sfgov.org"
instructions = "We're making a chatbot for all the helpful information about activities to do in San Francisco."

documents = client.run(url, instructions)

# Serialize the documents into JSON files
import json
import os

# Create output directory if it doesn't exist
output_dir = 'output_documents'
os.makedirs(output_dir, exist_ok=True)

# Save each document as a separate JSON file
for idx, doc in enumerate(documents):
    filename = f'document_{idx+1}.json'
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)

print('documents stored in', output_dir)
