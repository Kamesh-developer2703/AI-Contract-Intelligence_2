import json
from transformers import AutoTokenizer

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained("roberta-base")

# Load dataset
with open("data/processed/roberta_train.json", "r", encoding="utf-8") as f:
    data = json.load(f)

tokenized_data = []

for item in data:
    encoding = tokenizer(
        item["text"],
        truncation=True,
        padding="max_length",
        max_length=128
    )

    tokenized_data.append({
        "input_ids": encoding["input_ids"],
        "attention_mask": encoding["attention_mask"],
        "label": item["label"]
    })

# Save tokenized dataset
with open(
    "data/processed/tokenized_dataset.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(tokenized_data, f)

print("Total Tokenized Records:", len(tokenized_data))
print("First Tokenized Record:")
print(tokenized_data[0])