import json

with open(r"D:\Zoho\Zaalima_project\AI_Contract_Intelligence\data\cuad\CUADv1.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

first_para = dataset["data"][0]["paragraphs"][0]

print("Context Length:")
print(len(first_para["context"]))

print("\nNumber of Questions:")
print(len(first_para["qas"]))

print("\nFirst QA Keys:")
print(first_para["qas"][0].keys())