import json
import random

with open("data/processed/training_dataset.json","r",encoding="utf-8") as f:

    data=json.load(f)

sample=random.choice(data)

print("="*60)

print(sample)

print("="*60)