import json
import re

# Load processed dataset
with open("data/processed/training_dataset.json", "r", encoding="utf-8") as f:
    records = json.load(f)

# Store unique clause names
labels = set()

for record in records:

    clause = record["clause_type"]

    # Extract only the clause name inside quotes
    match = re.search(r'"([^"]+)"', clause)

    if match:
        clause_name = match.group(1).strip()
    else:
        clause_name = clause.strip()

    labels.add(clause_name)

# Sort labels for consistent IDs
labels = sorted(labels)

# Create label mapping
label_mapping = {
    label: idx
    for idx, label in enumerate(labels)
}

# Save mapping
with open("classifier/label_mapping.json", "w", encoding="utf-8") as f:
    json.dump(label_mapping, f, indent=4)

print("=" * 50)
print("Label Mapping Created Successfully")
print("=" * 50)
print("Total Labels :", len(label_mapping))
print()

for label, idx in label_mapping.items():
    print(f"{idx:2d} -> {label}")

print()
print("Saved to : classifier/label_mapping.json")
print("=" * 50)