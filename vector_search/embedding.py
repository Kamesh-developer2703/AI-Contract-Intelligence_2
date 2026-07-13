from sentence_transformers import SentenceTransformer

# Load embedding model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text: str):
    """
    Convert text into a vector embedding.
    """

    embedding = model.encode(text)

    return embedding.tolist()


if __name__ == "__main__":

    sample = "This agreement shall remain confidential."

    vector = generate_embedding(sample)

    print("Embedding Dimension :", len(vector))
    print(vector[:10])