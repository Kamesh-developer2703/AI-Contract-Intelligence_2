import json

with open("classifier/label_mapping.json","r",encoding="utf-8") as f:

    mapping = json.load(f)

print()

print("Total Labels :",len(mapping))

print()

for question,label in list(mapping.items())[:10]:

    print(label,"->",question)