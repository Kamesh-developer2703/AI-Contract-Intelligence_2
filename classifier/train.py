import os
import json
import torch
import argparse
import numpy as np
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)

def parse_args():
    parser = argparse.ArgumentParser(description="AI Contract Intelligence - Train RoBERTa Classifier")
    parser.add_argument("--fast", action="store_true", help="Enable fast CPU training mode")
    parser.add_argument("--no-fast", action="store_true", help="Disable fast training even on CPU")
    parser.add_argument("--epochs", type=int, default=5, help="Number of training epochs")
    return parser.parse_args()

def main():
    args = parse_args()
    
    cuda_available = torch.cuda.is_available()
    is_fast_mode = args.fast or (not cuda_available and not args.no_fast)
    
    print("=" * 60)
    print("AI Contract Intelligence - Training RoBERTa Classifier (Optimized)")
    print("=" * 60)
    print(f"CUDA Available : {cuda_available}")
    print(f"Fast Mode Enabled: {is_fast_mode}")
    
    # Paths
    train_path = "datasets/cuad_processed/train.json"
    val_path = "datasets/cuad_processed/val.json"
    model_name = "roberta-base"
    save_path = "models/roberta_contract_classifier"
    
    # 1. Load label mapping
    label_mapping_path = "classifier/label_mapping.json"
    with open(label_mapping_path, "r", encoding="utf-8") as f:
        label_to_id = json.load(f)
    num_labels = len(label_to_id)
    
    # 2. Load dataset splits
    with open(train_path, "r", encoding="utf-8") as f:
        train_records = json.load(f)
    with open(val_path, "r", encoding="utf-8") as f:
        val_records = json.load(f)
        
    # 3. Apply Fast Mode subsetting
    if is_fast_mode:
        print("\nFast mode: Selecting balanced subset (max 35 samples/class) for rapid CPU training...")
        train_subset = []
        val_subset = []
        
        for label_name, label_id in label_to_id.items():
            class_train_records = [r for r in train_records if r["clause_type"] == label_name]
            class_val_records = [r for r in val_records if r["clause_type"] == label_name]
            
            # Subsample
            train_subset.extend(class_train_records[:35])
            val_subset.extend(class_val_records[:10])
            
        train_records = train_subset
        val_records = val_subset
        
        # Shuffle subsets
        np.random.seed(42)
        np.random.shuffle(train_records)
        np.random.shuffle(val_records)
        
    print(f"Final training samples: {len(train_records)}")
    print(f"Final validation samples: {len(val_records)}")
    
    # Convert to HF dataset formats
    train_dataset = Dataset.from_dict({
        "text": [r["text"] for r in train_records],
        "label": [label_to_id[r["clause_type"]] for r in train_records]
    })
    val_dataset = Dataset.from_dict({
        "text": [r["text"] for r in val_records],
        "label": [label_to_id[r["clause_type"]] for r in val_records]
    })
    
    # 4. Initialize Tokenizer & Model
    print(f"\nLoading Pre-trained {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=num_labels
    )
    
    # 5. FREEZE ROBERTA BACKBONE for fast CPU training
    print("Freezing RoBERTa backbone encoder layers...")
    for name, param in model.roberta.named_parameters():
        param.requires_grad = False
        
    # 6. Tokenize datasets
    # Reduce max_length to 64 for speed on CPU
    def tokenize_fn(batch):
        return tokenizer(batch["text"], truncation=True, padding="max_length", max_length=64)
        
    print("Tokenizing datasets (max_length=64)...")
    train_tokenized = train_dataset.map(tokenize_fn, batched=True)
    val_tokenized = val_dataset.map(tokenize_fn, batched=True)
    
    # 7. Training Configuration
    epochs = args.epochs  # Defaults to 5
    batch_size = 32 if is_fast_mode else (16 if cuda_available else 8)
    learning_rate = 5e-3 if is_fast_mode else 3e-5
    
    training_args = TrainingArguments(
        output_dir="models/checkpoints",
        eval_strategy="epoch",
        save_strategy="no",
        learning_rate=learning_rate,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        num_train_epochs=epochs,
        weight_decay=0.01,
        logging_steps=5,
        report_to="none"
    )
    
    # Accuracy metric helper
    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        predictions = np.argmax(logits, axis=-1)
        acc = np.mean(predictions == labels)
        return {"accuracy": float(acc)}
        
    # 8. Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_tokenized,
        eval_dataset=val_tokenized,
        compute_metrics=compute_metrics
    )
    
    # 9. Start Fine-Tuning
    print("\n" + "=" * 60)
    print("STARTING TRAINING")
    print("=" * 60)
    trainer.train()
    print("Training Complete!")
    
    # Evaluate
    print("\nRunning Evaluation...")
    eval_res = trainer.evaluate()
    print(f"Validation accuracy: {eval_res.get('eval_accuracy', 0.0):.4f}")
    
    # 10. Save Fine-tuned Model & Tokenizer
    print(f"\nSaving fine-tuned model and tokenizer to: {save_path}")
    os.makedirs(save_path, exist_ok=True)
    trainer.save_model(save_path)
    tokenizer.save_pretrained(save_path)
    print("Model saved successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
