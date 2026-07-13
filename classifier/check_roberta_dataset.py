import json

with open("data/processed/roberta_train.json","r",encoding="utf-8") as f:
    data = json.load(f)

print("Total Records:", len(data))
print("First Record:", data[0])