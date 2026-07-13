import os
import json
import random
from sklearn.model_selection import train_test_split

# Configuration paths
DATASET_PATH = "data/processed/clean_training_dataset.json"
FALLBACK_DATASET_PATH = "data/processed/train.json"
RAW_CUAD_PATH = "data/cuad/CUADv1.json"
OUTPUT_DIR = "datasets/cuad_processed"
LABEL_MAPPING_PATH = "classifier/label_mapping.json"

# Target categories for our simplified classifier
TARGET_CATEGORIES = [
    "Liability",
    "Termination",
    "Indemnity",
    "Governing Law",
    "Confidentiality",
    "Payment Terms",
    "Assignment",
    "Non-Compete",
    "General Covenants"
]

# Map 41 CUAD classes to target simplified categories
CUAD_MAP = {
    "Cap On Liability": "Liability",
    "Uncapped Liability": "Liability",
    "Liquidated Damages": "Liability",
    
    "Termination For Convenience": "Termination",
    "Notice Period To Terminate Renewal": "Termination",
    
    "Governing Law": "Governing Law",
    
    "Payment Terms": "Payment Terms",
    "Revenue/Profit Sharing": "Payment Terms",
    "Price Restrictions": "Payment Terms",
    "Minimum Commitment": "Payment Terms",
    
    "Anti-Assignment": "Assignment",
    "Ip Ownership Assignment": "Assignment",
    
    "Non-Compete": "Non-Compete",
    "No-Solicit Of Customers": "Non-Compete",
    "No-Solicit Of Employees": "Non-Compete",
    "Competitive Restriction Exception": "Non-Compete",
    "Exclusivity": "Non-Compete",
    
    "Covenant Not To Sue": "Indemnity",
}

def load_data():
    """Load paragraph records, checking clean dataset first, then raw CUAD."""
    records = []
    
    # Method 1: Load pre-split paragraph json files if available
    for path in [DATASET_PATH, FALLBACK_DATASET_PATH]:
        if os.path.exists(path):
            print(f"Loading paragraph dataset from: {path}")
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for item in data:
                    text = item.get("clause_text") or item.get("text")
                    clause_type = item.get("clause_type") or item.get("label")
                    if text and clause_type:
                        records.append({
                            "text": text.strip(),
                            "original_type": str(clause_type)
                        })
                if records:
                    return records
            except Exception as e:
                print(f"Failed to load {path}: {e}")
                
    # Method 2: Extract paragraphs from raw CUADv1.json
    if os.path.exists(RAW_CUAD_PATH):
        print(f"Extracting paragraphs from raw CUAD JSON: {RAW_CUAD_PATH}")
        try:
            with open(RAW_CUAD_PATH, "r", encoding="utf-8") as f:
                cuad = json.load(f)
            
            for contract in cuad.get("data", []):
                title = contract.get("title", "")
                for paragraph in contract.get("paragraphs", []):
                    context = paragraph.get("context", "")
                    # Extract qa annotations to label clauses
                    for qa in paragraph.get("qas", []):
                        question = qa.get("question", "")
                        # Try to parse question name (e.g. from 'Highlight ... related to "Governing Law"')
                        q_type = "General Covenants"
                        for cat in CUAD_MAP.keys():
                            if cat.lower() in question.lower():
                                q_type = cat
                                break
                                
                        for ans in qa.get("answers", []):
                            ans_text = ans.get("text", "").strip()
                            if len(ans_text) >= 30:
                                records.append({
                                    "text": ans_text,
                                    "original_type": q_type
                                })
            return records
        except Exception as e:
            print(f"Failed to parse raw CUAD: {e}")
            
    return records

def preprocess_and_map(records):
    """Map original CUAD categories to simplified contract categories with text keyword mapping."""
    processed = []
    
    for r in records:
        text = r["text"]
        text_lower = text.lower()
        orig = r["original_type"]
        
        # Primary mapping: original category
        mapped_type = CUAD_MAP.get(orig, "General Covenants")
        
        # Refine/override category based on text keyword search to capture specific legal variations
        if "indemnify" in text_lower or "hold harmless" in text_lower or "defend" in text_lower:
            mapped_type = "Indemnity"
        elif "unlimited liability" in text_lower or "uncapped liability" in text_lower:
            mapped_type = "Liability"
        elif "terminate" in text_lower or "termination" in text_lower:
            if orig in ["Termination For Convenience", "Notice Period To Terminate Renewal", "General Covenants"]:
                mapped_type = "Termination"
        elif "confidential" in text_lower or "non-disclosure" in text_lower:
            if orig in ["General Covenants"]:
                mapped_type = "Confidentiality"
                
        processed.append({
            "text": text,
            "clause_type": mapped_type
        })
        
    return processed

def main():
    print("=" * 60)
    print("AI Contract Intelligence - Preprocessing Dataset")
    print("=" * 60)
    
    # 1. Load data
    records = load_data()
    if not records:
        print("Error: No CUAD training data found. Preprocessing aborted.")
        return
        
    print(f"Loaded {len(records)} raw clause records.")
    
    # 2. Map labels
    processed = preprocess_and_map(records)
    
    # Filter short paragraphs
    processed = [p for p in processed if len(p["text"]) >= 30]
    print(f"Filtered to {len(processed)} meaningful paragraph samples.")
    
    # 3. Create and save label mapping automatically
    label_to_id = {name: idx for idx, name in enumerate(TARGET_CATEGORIES)}
    
    os.makedirs(os.path.dirname(LABEL_MAPPING_PATH), exist_ok=True)
    with open(LABEL_MAPPING_PATH, "w", encoding="utf-8") as f:
        json.dump(label_to_id, f, indent=4)
    print(f"Saved label mapping to: {LABEL_MAPPING_PATH}")
    print("Label mapping:", label_to_id)
    
    # 4. Generate splits
    texts = [p["text"] for p in processed]
    labels = [label_to_id[p["clause_type"]] for p in processed]
    
    train_idx, val_idx = train_test_split(
        range(len(processed)), 
        test_size=0.15, 
        random_state=42, 
        stratify=labels
    )
    
    train_data = [processed[i] for i in train_idx]
    val_data = [processed[i] for i in val_idx]
    
    print(f"Training split size: {len(train_data)}")
    print(f"Validation split size: {len(val_data)}")
    
    # Count distribution
    dist = {}
    for item in train_data:
        dist[item["clause_type"]] = dist.get(item["clause_type"], 0) + 1
    print("\nClass distribution in train split:")
    for k, v in dist.items():
        print(f"  {k}: {v}")
        
    # Save splits
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    with open(os.path.join(OUTPUT_DIR, "train.json"), "w", encoding="utf-8") as f:
        json.dump(train_data, f, indent=4)
        
    with open(os.path.join(OUTPUT_DIR, "val.json"), "w", encoding="utf-8") as f:
        json.dump(val_data, f, indent=4)
        
    print(f"\nPreprocessing finished. Data written to: {OUTPUT_DIR}")
    print("=" * 60)

if __name__ == "__main__":
    main()
