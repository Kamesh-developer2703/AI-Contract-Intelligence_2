import json

DATASET = "data/processed/training_dataset.json"

with open(DATASET, "r", encoding="utf-8") as f:
    data = json.load(f)

missing = 0

for i, row in enumerate(data):

    if not row.get("clause_text"):

        missing += 1

        print("Missing clause text:", i)

    if not row.get("clause_type"):

        missing += 1

        print("Missing label:", i)

print()

print("Total Records :", len(data))
print("Missing Fields :", missing)