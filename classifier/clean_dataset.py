import json
import re
from collections import Counter

INPUT_FILE = "data/processed/training_dataset.json"
OUTPUT_FILE = "data/processed/clean_training_dataset.json"

print("=" * 60)
print("Cleaning CUAD Training Dataset")
print("=" * 60)

# -----------------------------
# Load dataset
# -----------------------------
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    records = json.load(f)

print("Original Records :", len(records))

clean_records = []

# -----------------------------
# Clean every record
# -----------------------------
for record in records:

    clause_question = record["clause_type"]
    clause_text = record["clause_text"]
    title = record["title"]

    # Extract text inside quotes
    match = re.search(r'"([^"]+)"', clause_question)

    if match:
        clause_name = match.group(1).strip()
    else:
        clause_name = clause_question.strip()

    clean_records.append({
        "title": title,
        "clause_type": clause_name,
        "clause_text": clause_text
    })

# -----------------------------
# Save cleaned dataset
# -----------------------------
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(clean_records, f, indent=4)

print()
print("Clean dataset saved successfully.")
print("Output :", OUTPUT_FILE)

# -----------------------------
# Statistics
# -----------------------------
labels = [x["clause_type"] for x in clean_records]

counter = Counter(labels)

print()
print("=" * 60)
print("Dataset Statistics")
print("=" * 60)

print("Total Records :", len(clean_records))
print("Unique Labels :", len(counter))

print()
print("Labels Found")
print("-" * 60)

for i, label in enumerate(sorted(counter.keys()), start=1):
    print(f"{i:02d}. {label:35} -> {counter[label]}")

print()
print("=" * 60)
print("First Clean Record")
print("=" * 60)

print(json.dumps(clean_records[0], indent=4))

print()
print("=" * 60)
print("Cleaning Completed Successfully")
print("=" * 60)