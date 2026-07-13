import json
import os
import numpy as np
import torch

from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

# =====================================================
# CONFIGURATION
# =====================================================

DATASET_PATH = "data/processed/clean_training_dataset.json"

LABEL_MAPPING_PATH = "classifier/label_mapping.json"

MODEL_NAME = "roberta-base"

SAVE_MODEL_PATH = "models/roberta_contract_classifier"

MAX_LENGTH = 128

print("=" * 60)
print("AI Contract Intelligence - RoBERTa Training")
print("=" * 60)

# =====================================================
# DEVICE
# =====================================================

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("Device :", device)

# =====================================================
# LOAD DATASET
# =====================================================

print("\nLoading Dataset...")

with open(DATASET_PATH, "r", encoding="utf-8") as f:
    records = json.load(f)

print("Total Records :", len(records))

# =====================================================
# LOAD LABEL MAPPING
# =====================================================

print("\nLoading Label Mapping...")

with open(LABEL_MAPPING_PATH, "r", encoding="utf-8") as f:
    label_to_id = json.load(f)

id_to_label = {}

for label, idx in label_to_id.items():
    id_to_label[str(idx)] = label

print("Total Labels :", len(label_to_id))

# =====================================================
# PREPARE TEXT + LABEL
# =====================================================

texts = []
labels = []

print("\nPreparing Dataset...")

for record in records:

    text = record["clause_text"].strip()

    label_name = record["clause_type"]

    label_id = label_to_id[label_name]

    texts.append(text)

    labels.append(label_id)

print("Prepared Samples :", len(texts))

print()

print("Sample")

print("-" * 60)

print("Text :")

print(texts[0])

print()

print("Label :", labels[0])

print("Label Name :", id_to_label[str(labels[0])])

# =====================================================
# CREATE HUGGINGFACE DATASET
# =====================================================

dataset = Dataset.from_dict({

    "text": texts,

    "label": labels

})

print("\nDataset Created Successfully")

print(dataset)

# =====================================================
# LOAD TOKENIZER
# =====================================================

print("\nLoading Tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

print("Tokenizer Loaded")

# =====================================================
# TOKENIZATION FUNCTION
# =====================================================

def tokenize(batch):

    return tokenizer(

        batch["text"],

        truncation=True,

        padding="max_length",

        max_length=MAX_LENGTH

    )

print("\nTokenizing Dataset...")

tokenized_dataset = dataset.map(

    tokenize,

    batched=True

)

print("Tokenization Completed")

print(tokenized_dataset)

print()

print("=" * 60)
print("PART 1 COMPLETED SUCCESSFULLY")
print("=" * 60)

# =====================================================
# TRAIN / VALIDATION SPLIT
# =====================================================

import evaluate

print("\nSplitting Dataset...")

dataset_split = tokenized_dataset.train_test_split(
    test_size=0.2,
    seed=42
)

train_dataset = dataset_split["train"]

eval_dataset = dataset_split["test"]

print("Training Samples :", len(train_dataset))
print("Validation Samples :", len(eval_dataset))


# =====================================================
# LOAD MODEL
# =====================================================

print("\nLoading RoBERTa Model...")

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=len(label_to_id)
)

model.to(device)

print("Model Loaded Successfully")

# =====================================================
# METRICS
# =====================================================

accuracy_metric = evaluate.load("accuracy")
precision_metric = evaluate.load("precision")
recall_metric = evaluate.load("recall")
f1_metric = evaluate.load("f1")

def compute_metrics(eval_pred):

    logits, labels = eval_pred

    predictions = np.argmax(logits, axis=-1)

    accuracy = accuracy_metric.compute(
        predictions=predictions,
        references=labels
    )

    precision = precision_metric.compute(
        predictions=predictions,
        references=labels,
        average="weighted"
    )

    recall = recall_metric.compute(
        predictions=predictions,
        references=labels,
        average="weighted"
    )

    f1 = f1_metric.compute(
        predictions=predictions,
        references=labels,
        average="weighted"
    )

    return {
        "accuracy": accuracy["accuracy"],
        "precision": precision["precision"],
        "recall": recall["recall"],
        "f1": f1["f1"]
    }

print("Metrics Loaded Successfully")

# =====================================================
# TRAINING ARGUMENTS
# =====================================================

from transformers import TrainingArguments

training_args = TrainingArguments(
    output_dir="models/checkpoints",

    eval_strategy="epoch",
    save_strategy="epoch",

    learning_rate=2e-5,

    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,

    num_train_epochs=5,

    weight_decay=0.01,

    logging_dir="logs",
    logging_steps=100,

    load_best_model_at_end=True,

    metric_for_best_model="accuracy",

    report_to="none"
)

print("\nTraining Configuration Ready")

print("=" * 60)
print("PART 2 COMPLETED SUCCESSFULLY")
print("=" * 60)

# =====================================================
# TRAINER
# =====================================================

from transformers import Trainer

print("\nCreating Trainer...")

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    compute_metrics=compute_metrics,
)

print("Trainer Created Successfully")

# =====================================================
# TRAIN MODEL
# =====================================================

print("\n" + "=" * 60)
print("STARTING TRAINING")
print("=" * 60)

trainer.train()

print("\nTraining Completed Successfully!")

# =====================================================
# EVALUATE MODEL
# =====================================================

print("\nEvaluating Model...")

results = trainer.evaluate()

print("\nEvaluation Results")

for key, value in results.items():
    print(f"{key} : {value}")

# =====================================================
# SAVE MODEL
# =====================================================

print("\nSaving Model...")

os.makedirs(SAVE_MODEL_PATH, exist_ok=True)

trainer.save_model(SAVE_MODEL_PATH)

tokenizer.save_pretrained(SAVE_MODEL_PATH)

print("Model Saved Successfully!")

print("Location :", SAVE_MODEL_PATH)

# =====================================================
# FINISHED
# =====================================================

print("\n" + "=" * 60)
print("AI CONTRACT CLASSIFIER TRAINING COMPLETED")
print("=" * 60)