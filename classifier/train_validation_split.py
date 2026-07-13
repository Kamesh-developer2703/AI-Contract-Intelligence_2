import json
import random

# Load dataset
with open("data/processed/training_dataset.json", "r", encoding="utf-8") as f:
    records = json.load(f)

# Shuffle records
random.shuffle(records)

# 80-20 split
split_index = int(len(records) * 0.8)

train_data = records[:split_index]
validation_data = records[split_index:]

# Save train dataset
with open("data/processed/train.json", "w", encoding="utf-8") as f:
    json.dump(train_data, f, indent=4)

# Save validation dataset
with open("data/processed/validation.json", "w", encoding="utf-8") as f:
    json.dump(validation_data, f, indent=4)

print("Train Records:", len(train_data))
print("Validation Records:", len(validation_data))