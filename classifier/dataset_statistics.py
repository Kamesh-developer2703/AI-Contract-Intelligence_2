import json

with open("data/processed/training_dataset.json", "r", encoding="utf-8") as f:
    records = json.load(f)

stats = {
    "total_records": len(records)
}

with open("data/processed/dataset_statistics.json", "w", encoding="utf-8") as f:
    json.dump(stats, f, indent=4)

print(stats)