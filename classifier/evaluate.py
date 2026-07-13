import os
import json
import torch
import numpy as np
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer
from sklearn.metrics import classification_report, accuracy_score, precision_recall_fscore_support

def main():
    print("=" * 60)
    print("AI Contract Intelligence - Model Evaluation")
    print("=" * 60)
    
    val_path = "datasets/cuad_processed/val.json"
    model_path = "models/roberta_contract_classifier"
    label_mapping_path = "classifier/label_mapping.json"
    
    # Check if model exists
    if not os.path.exists(model_path) or not os.path.exists(os.path.join(model_path, "pytorch_model.bin")) and not os.path.exists(os.path.join(model_path, "model.safetensors")):
        print(f"Error: Trained model weights not found at: {model_path}")
        print("Please run training first: python classifier/train.py --fast")
        return
        
    # 1. Load label mapping
    with open(label_mapping_path, "r", encoding="utf-8") as f:
        label_to_id = json.load(f)
    id_to_label = {v: k for k, v in label_to_id.items()}
    num_labels = len(label_to_id)
    
    # 2. Load validation dataset
    if not os.path.exists(val_path):
        print(f"Error: Validation data not found at: {val_path}")
        return
        
    with open(val_path, "r", encoding="utf-8") as f:
        val_records = json.load(f)
        
    print(f"Loaded {len(val_records)} validation samples.")
    
    # Convert to HF Dataset
    val_dataset = Dataset.from_dict({
        "text": [r["text"] for r in val_records],
        "label": [label_to_id[r["clause_type"]] for r in val_records]
    })
    
    # 3. Load model and tokenizer
    print("Loading fine-tuned model and tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    
    # 4. Tokenize dataset
    def tokenize_fn(batch):
        return tokenizer(batch["text"], truncation=True, padding="max_length", max_length=64)
        
    val_tokenized = val_dataset.map(tokenize_fn, batched=True)
    
    # 5. Predict using Trainer
    trainer = Trainer(model=model)
    print("Running predictions on validation split...")
    predictions = trainer.predict(val_tokenized)
    
    logits = predictions.predictions
    preds = np.argmax(logits, axis=-1)
    labels = predictions.label_ids
    
    # 6. Calculate metrics
    acc = accuracy_score(labels, preds)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average="weighted")
    
    print("\n" + "=" * 60)
    print("EVALUATION RESULTS")
    print("=" * 60)
    print(f"Accuracy:      {acc:.4f}  (Target: 80%+) ")
    print(f"Precision:     {precision:.4f}")
    print(f"Recall:        {recall:.4f}")
    print(f"F1 Score (W):  {f1:.4f}  (Target: 0.80+) ")
    print("=" * 60)
    
    # Generate detailed classification report
    target_names = [id_to_label[i] for i in range(num_labels)]
    report = classification_report(
        labels,
        preds,
        target_names=target_names,
        labels=range(num_labels),
        zero_division=0
    )
    print("\nDetailed Classification Report:")
    print(report)
    
    # Save evaluation report to evaluation_report.md
    report_path = "classifier/evaluation_report.md"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Model Evaluation Report\n\n")
        f.write("Evaluation results on the validation split.\n\n")
        f.write("## Summary Metrics\n\n")
        f.write("| Metric | Score |\n")
        f.write("| :--- | :--- |\n")
        f.write(f"| **Accuracy** | {acc:.4f} |\n")
        f.write(f"| **Precision (Weighted)** | {precision:.4f} |\n")
        f.write(f"| **Recall (Weighted)** | {recall:.4f} |\n")
        f.write(f"| **F1 Score (Weighted)** | {f1:.4f} |\n\n")
        f.write("## Detailed Classification Report\n\n")
        f.write("```text\n")
        f.write(report)
        f.write("```\n")
    print(f"Saved evaluation report to: {report_path}")
    print("=" * 60)

if __name__ == "__main__":
    main()
