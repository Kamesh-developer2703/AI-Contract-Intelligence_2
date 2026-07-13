import json

with open("data/processed/training_dataset.json", "r", encoding="utf-8") as f:
    records = json.load(f)

print(records[0])