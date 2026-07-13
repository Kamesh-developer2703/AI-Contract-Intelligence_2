from transformers import AutoTokenizer, AutoModel
import torch

print("Loading RoBERTa...")

tokenizer = AutoTokenizer.from_pretrained("roberta-base")
model = AutoModel.from_pretrained("roberta-base")

contract_clause = """
This agreement shall automatically renew for an additional one-year term unless either party provides written notice of termination.
"""

inputs = tokenizer(
    contract_clause,
    return_tensors="pt",
    truncation=True,
    padding=True,
    max_length=128
)

with torch.no_grad():
    outputs = model(**inputs)

embedding = outputs.last_hidden_state.mean(dim=1)

print("Embedding Shape:", embedding.shape)
print("Embedding Generated Successfully!")