from transformers import AutoTokenizer, AutoModel
import torch
from torch.nn.functional import cosine_similarity

print("Loading RoBERTa...")

tokenizer = AutoTokenizer.from_pretrained("roberta-base")
model = AutoModel.from_pretrained("roberta-base")

clause1 = "This agreement may be terminated with 30 days written notice."

clause2 = "Either party can end the contract by giving 30 days notice."

clause3 = "Payment shall be made within 15 business days."

def get_embedding(text):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    with torch.no_grad():
        outputs = model(**inputs)

    return outputs.last_hidden_state.mean(dim=1)

emb1 = get_embedding(clause1)
emb2 = get_embedding(clause2)
emb3 = get_embedding(clause3)

sim1 = cosine_similarity(emb1, emb2).item()
sim2 = cosine_similarity(emb1, emb3).item()

print("\nClause 1 vs Clause 2 Similarity:", round(sim1, 4))
print("Clause 1 vs Clause 3 Similarity:", round(sim2, 4))