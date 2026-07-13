import json
from collections import Counter

DATASET = "data/processed/training_dataset.json"

with open(DATASET, "r", encoding="utf-8") as f:
    data = json.load(f)

print("=" * 50)
print("Dataset Statistics")
print("=" * 50)

print("Total Records :", len(data))

labels = []

for item in data:

    if "clause_type" in item:
        labels.append(item["clause_type"])

counter = Counter(labels)

print("\nClause Distribution\n")

for label, count in sorted(counter.items()):
    print(f"{label:35} {count}")

print("\nTotal Classes :", len(counter))

print("\nTop 5 Most Common Classes:")
for label, count in counter.most_common(5):
    print(f"{label}: {count}")

print("\nTop 5 Least Common Classes:")
for label, count in counter.most_common()[-5:]:
    print(f"{label}: {count}")