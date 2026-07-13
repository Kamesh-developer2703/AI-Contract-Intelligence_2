from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Dummy example
y_true = [0, 1, 2, 1, 0]
y_pred = [0, 1, 2, 0, 0]

print("Accuracy:", accuracy_score(y_true, y_pred))
print("Precision:", precision_score(y_true, y_pred, average="weighted"))
print("Recall:", recall_score(y_true, y_pred, average="weighted"))
print("F1 Score:", f1_score(y_true, y_pred, average="weighted"))