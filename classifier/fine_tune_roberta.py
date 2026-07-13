import json
from sklearn.model_selection import train_test_split

with open("data/processed/tokenized_dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Total Records:", len(data))

train_data, val_data = train_test_split(
    data,
    test_size=0.2,
    random_state=42
)

print("Training Records:", len(train_data))
print("Validation Records:", len(val_data))

print("\nDataset Split Successful!")