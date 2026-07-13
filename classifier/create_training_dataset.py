import json

INPUT_FILE = "data/processed/clean_training_dataset.json"
OUTPUT_FILE = "classifier/label_mapping.json"

print("=" * 60)
print("Generating Label Mapping")
print("=" * 60)

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    records = json.load(f)

labels = sorted(set(record["clause_type"] for record in records))

label_to_id = {
    label: idx
    for idx, label in enumerate(labels)
}

id_to_label = {
    idx: label
    for idx, label in enumerate(labels)
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(
        {
            "label_to_id": label_to_id,
            "id_to_label": id_to_label
        },
        f,
        indent=4
    )

print()

print("Total Labels :", len(labels))
print()

for idx, label in enumerate(labels):
    print(f"{idx:02d} -> {label}")

print()

print("Saved Successfully!")
print("Location :", OUTPUT_FILE)