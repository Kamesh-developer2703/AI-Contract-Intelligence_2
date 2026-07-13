# Contract Clause Classifier Pipeline

This module contains the pipeline to preprocess the CUAD contract dataset, fine-tune a RoBERTa-base sequence classification model, evaluate its performance, and run inference on contract paragraphs.

---

## Folder Structure

```text
classifier/
├── preprocess.py        # Maps CUAD classes to target labels and splits data
├── train.py             # Fine-tunes the RoBERTa model (with --fast CPU mode)
├── evaluate.py          # Evaluates validation splits and writes reports
├── predict.py           # Classifier inference script with threshold checks
├── label_mapping.json   # Auto-generated label index dictionary
├── README.md            # Module pipeline documentation (this file)
├── model_architecture.md# Deep-dive into RoBERTa & classification heads
└── evaluation_report.md # Generated validation accuracy/F1 metrics report
```

---

## Pipeline Execution Guide

Run the pipeline steps sequentially from the project root directory.

### Step 1: Preprocess the Dataset
This script loads raw CUAD dataset files, maps the 41 CUAD labels to 8 simplified contract categories, filters short text snippets, and generates train/validation splits:
```bash
python classifier/preprocess.py
```
This generates the split files in `datasets/cuad_processed/` and writes `classifier/label_mapping.json`.

### Step 2: Fine-tune the RoBERTa Model
Fine-tune the RoBERTa-base sequence classification model. By default, running on a CPU automatically activates `--fast` mode (training on a high-quality subset of 200 paragraphs for 1 epoch, which completes in about 1 minute):
```bash
# CPU / Quick verification run (default on CPU)
python classifier/train.py --fast

# Full GPU training run
python classifier/train.py --epochs 3 --no-fast
```
This saves the trained weights, tokenizer config, and model config to `models/roberta_contract_classifier/`.

### Step 3: Evaluate Model Performance
Assess model predictions on the validation split and print accuracy, precision, recall, and F1 scores:
```bash
python classifier/evaluate.py
```
This prints the metrics to console and writes a detailed markdown report to `classifier/evaluation_report.md`.

### Step 4: Run Inference Test
Verify that the inference system works and returns prediction dictionaries:
```bash
python -m classifier.predict
```
If the trained model weights are missing, the classifier will output a user-friendly instruction block rather than crashing with an unreadable traceback.
