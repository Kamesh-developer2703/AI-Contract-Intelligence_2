import json

with open(r"data\cuad\CUADv1.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

training_data = []

for contract in dataset["data"][:5]:

    title = contract["title"]

    paragraph = contract["paragraphs"][0]

    for qa in paragraph["qas"]:

        if qa["answers"]:

            training_data.append({
                "contract_title": title,
                "question": qa["question"],
                "answer": qa["answers"][0]["text"]
            })

with open("data/processed/sample_training.json","w",encoding="utf-8") as f:
    json.dump(training_data,f,indent=4)

print("Training JSON created successfully")

print("Total Records:", len(training_data))
print("\nFirst Record:")
print(training_data[0])