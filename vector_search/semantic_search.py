from sentence_transformers import SentenceTransformer
from vector_search.pinecone_db import index

# Load embedding model once
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def semantic_search(query, top_k=5):
    """
    Search similar contract clauses using Pinecone.
    """

    # Convert query into embedding
    query_embedding = model.encode(query).tolist()

    # Search Pinecone
    response = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    results = []

    for match in response["matches"]:
        results.append({
            "score": round(match["score"], 4),
            "title": match["metadata"]["title"],
            "clause_type": match["metadata"]["clause_type"],
            "text": match["metadata"]["text"]
        })

    return results


if __name__ == "__main__":

    query = "termination clause"

    results = semantic_search(query)

    print("=" * 60)
    print("Semantic Search Results")
    print("=" * 60)

    for i, result in enumerate(results, start=1):
        print(f"\nResult {i}")
        print("Similarity :", result["score"])
        print("Title      :", result["title"])
        print("Clause     :", result["clause_type"])
        print("Text       :", result["text"])