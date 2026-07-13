import os
from dotenv import load_dotenv
from pinecone import Pinecone

# Load .env file
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY not found in .env")

if not PINECONE_INDEX:
    raise ValueError("PINECONE_INDEX not found in .env")

# Create Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Connect to existing index
index = pc.Index(PINECONE_INDEX)

print("=" * 50)
print("Connected Successfully to Pinecone")
print("Index :", PINECONE_INDEX)
print("=" * 50)