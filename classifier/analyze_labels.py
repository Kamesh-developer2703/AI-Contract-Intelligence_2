import json
from collections import Counter

with open("data/processed/roberta_train.json", "r", encoding="utf-8") as f:
    data = json.load(f)

labels = [item["label"] for item in data]

label_counts = Counter(labels)

print("Total Records:", len(data))
print("Total Unique Labels:", len(label_counts))

print("\nTop 10 Labels:")
for label, count in label_counts.most_common(10):
    print(f"Label {label}: {count}")