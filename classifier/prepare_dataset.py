import json

with open("data/processed/train.json", "r", encoding="utf-8") as f:
    train_data = json.load(f)

with open("classifier/label_mapping.json", "r", encoding="utf-8") as f:
    label_mapping = json.load(f)

prepared_data = []

for item in train_data:

    prepared_data.append({
        "text": item["clause_text"],
        "label": label_mapping[item["clause_type"]]
    })

with open(
    "data/processed/roberta_train.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(prepared_data, f, indent=4)

print("Prepared Records:", len(prepared_data))
print("First Record:", prepared_data[0])