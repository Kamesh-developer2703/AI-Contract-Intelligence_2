import json

with open(r"data\cuad\CUADv1.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

first_para = dataset["data"][0]["paragraphs"][0]

print("Number of Questions:", len(first_para["qas"]))

first_qa = first_para["qas"][0]

print("\nQuestion:")
print(first_qa["question"])

print("\nAnswer:")
print(first_qa["answers"])

print("\nQA Keys:")
print(first_qa.keys())