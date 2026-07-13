import json
import uuid

from vector_search.embedding import generate_embedding
from vector_search.pinecone_db import index

DATASET_PATH = "data/processed/clean_training_dataset.json"

BATCH_SIZE = 100


def load_dataset():

    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def upload_vectors():

    data = load_dataset()

    print("=" * 60)
    print("Uploading vectors to Pinecone")
    print("=" * 60)

    vectors = []

    total = len(data)

    for i, record in enumerate(data):

        text = record["clause_text"]

        embedding = generate_embedding(text)

        vector = {

            "id": str(uuid.uuid4()),

            "values": embedding,

            "metadata": {

                "title": record["title"],

                "clause_type": record["clause_type"],

                "text": text

            }

        }

        vectors.append(vector)

        if len(vectors) == BATCH_SIZE:

            index.upsert(vectors=vectors)

            print(f"Uploaded {i+1}/{total}")

            vectors = []

    if vectors:

        index.upsert(vectors=vectors)

    print("=" * 60)
    print("Upload Completed Successfully")
    print(f"Total Uploaded : {total}")
    print("=" * 60)


if __name__ == "__main__":

    upload_vectors()