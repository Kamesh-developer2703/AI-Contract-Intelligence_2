import json

# Load dataset
with open("data/processed/roberta_train.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Evaluation Setup")

print("Total Records:", len(data))

# Sample records
print("\nSample Records:")
for i in range(3):
    print(f"\nRecord {i+1}")
    print("Text:", data[i]["text"][:100], "...")
    print("Label:", data[i]["label"])

print("\nEvaluation Metrics Planned:")
print("- Accuracy")
print("- Precision")
print("- Recall")
print("- F1 Score")

print("\nEvaluation Workflow Ready!")