import os
import json
import torch
import sys
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Configuration paths
MODEL_PATH = "models/roberta_contract_classifier"
LABEL_MAPPING_PATH = "classifier/label_mapping.json"
APP_ENV = os.getenv("APP_ENV", "development")

# Global cache for model and tokenizer
_tokenizer = None
_model = None
_id_to_label = None

def check_weights_exist() -> bool:
    """Check if fine-tuned weights exist in the model directory."""
    if os.path.exists(MODEL_PATH):
        for filename in ["pytorch_model.bin", "model.safetensors"]:
            if os.path.exists(os.path.join(MODEL_PATH, filename)):
                return True
    return False

def load_resources():
    """Load model, tokenizer, and label mapping, enforcing deployment rules."""
    global _tokenizer, _model, _id_to_label

    # 1. Load label mapping
    if _id_to_label is None:
        if not os.path.exists(LABEL_MAPPING_PATH):
            raise FileNotFoundError(f"Label mapping JSON file missing at: {LABEL_MAPPING_PATH}")
        with open(LABEL_MAPPING_PATH, "r", encoding="utf-8") as f:
            mapping = json.load(f)
        # Convert classname -> idx map into idx -> classname
        _id_to_label = {int(v): k for k, v in mapping.items()}

    # 2. Load model & tokenizer
    if _tokenizer is None or _model is None:
        if not check_weights_exist():
            err_msg = (
                "\n============================================================\n"
                "Fine-tuned model not found.\n\n"
                "Run:\n"
                "python classifier/preprocess.py\n"
                "python classifier/train.py --fast\n\n"
                "to generate the classifier.\n"
                "============================================================\n"
            )
            if APP_ENV == "production":
                raise FileNotFoundError(f"Trained model weights missing in production mode. {err_msg}")
            else:
                print(err_msg, file=sys.stderr)
                raise RuntimeError(err_msg)

        # Load weights
        try:
            _tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
            _model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            _model.to(device)
            _model.eval()
        except Exception as e:
            raise RuntimeError(f"Failed to load fine-tuned model resources: {e}")

def predict_clause(text: str) -> dict:
    """
    Predicts contract clause type using the fine-tuned RoBERTa model.
    Enforces confidence thresholding and returns rich risk explainability data.
    """
    if not text or not isinstance(text, str) or len(text.strip()) < 30:
        return {
            "clause_type": "Unknown Clause",
            "confidence": 0.0,
            "matched_text": text or "",
            "reason": "Paragraph too short or empty for classification",
            "severity": "Low",
            "risk_points": 0
        }

    # Ensure model resources are loaded
    load_resources()

    try:
        device = next(_model.parameters()).device
        inputs = _tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=256,
            return_tensors="pt"
        )
        # Move inputs to device
        inputs = {k: v.to(device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = _model(**inputs)
        
        # Get raw logits from the model
        logits = outputs.logits[0].clone()
        
        # Dynamic hybrid enhancement: Combine model outputs with keyword boosts
        # applied directly to logits before softmax to ensure robust accuracy.
        text_lower = text.lower()
        label_to_index = {name: idx for idx, name in _id_to_label.items()}
        
        # Apply boosts to raw logits (reduced from +10.0 to +2.5 to balance model influence)
        boost = 2.5
        
        liability_keywords = ["liability", "liable", "limit", "limitation", "exceed", "aggregate", "cap", "capped", "uncapped", "maximum", "consequential", "punitive"]
        termination_keywords = ["terminate", "termination", "notice", "convenience", "without cause", "material breach", "default", "cure period", "expiry", "expiration", "renew", "renewal"]
        indemnity_keywords = ["indemnify", "indemnity", "indemnification", "hold harmless", "defend", "harmless", "losses", "claims"]
        gov_keywords = ["governing law", "jurisdiction", "exclusive jurisdiction", "laws of", "courts of", "dispute", "arbitration", "venue", "forum"]
        conf_keywords = ["confidential", "confidentiality", "non-disclosure", "disclose", "disclosure", "proprietary", "secret", "secrets", "trade secret"]
        payment_keywords = ["payment", "invoice", "fee", "compensate", "compensation", "salary", "remuneration", "installment", "paid", "payable", "consideration", "rate", "price", "pricing", "billing", "bill", "lpa", "usd", "inr", "monthly", "annual"]
        assignment_keywords = ["assign", "assignment", "transfer", "successor", "successors", "consent of"]
        noncompete_keywords = ["non-compete", "compete", "solicit", "no-solicit", "non-solicitation", "restrictive", "covenant"]
        
        if any(k in text_lower for k in liability_keywords):
            if "Liability" in label_to_index:
                logits[label_to_index["Liability"]] += boost
        if any(k in text_lower for k in termination_keywords):
            if "Termination" in label_to_index:
                logits[label_to_index["Termination"]] += boost
        if any(k in text_lower for k in indemnity_keywords):
            if "Indemnity" in label_to_index:
                logits[label_to_index["Indemnity"]] += boost
        if any(k in text_lower for k in gov_keywords):
            if "Governing Law" in label_to_index:
                logits[label_to_index["Governing Law"]] += boost
        if any(k in text_lower for k in conf_keywords):
            if "Confidentiality" in label_to_index:
                logits[label_to_index["Confidentiality"]] += boost
        if any(k in text_lower for k in payment_keywords):
            if "Payment Terms" in label_to_index:
                logits[label_to_index["Payment Terms"]] += boost
        if any(k in text_lower for k in assignment_keywords):
            if "Assignment" in label_to_index:
                logits[label_to_index["Assignment"]] += boost
        if any(k in text_lower for k in noncompete_keywords):
            if "Non-Compete" in label_to_index:
                logits[label_to_index["Non-Compete"]] += boost
                
        # Now apply softmax to the boosted logits
        probabilities = torch.softmax(logits, dim=-1)
        confidence, predicted_idx = torch.max(probabilities, dim=-1)
        
        predicted_idx = predicted_idx.item()
        confidence = round(confidence.item(), 4)

        # Get label name
        clause_type = _id_to_label.get(predicted_idx, "Unknown Clause")

        # Threshold Check: If confidence < 0.60, return Unknown Clause
        if confidence < 0.60:
            clause_type = "Unknown Clause"
            confidence = 0.0

        # Assess risk attributes based on text matches and clause prediction
        severity = "Low"
        risk_points = 0
        reason = "Standard contractual clause"

        # Dynamic routing for Intellectual Property
        if clause_type in ["General Covenants", "Confidentiality", "Unknown Clause"]:
            if any(k in text_lower for k in ["ip", "intellectual property", "copyright", "patent", "trademark", "work for hire", "invention", "ownership"]):
                clause_type = "Intellectual Property"

        if clause_type == "Liability":
            if any(k in text_lower for k in ["unlimited", "uncapped", "no limit", "no cap", "liable for all"]):
                severity = "High"
                risk_points = 30
                reason = "Unlimited liability detected"
            elif any(k in text_lower for k in ["cap", "capped", "not exceed", "shall not exceed"]):
                severity = "Medium"
                risk_points = 5
                reason = "Liability cap detected"
            elif "insurance" in text_lower:
                severity = "Low"
                risk_points = 2
                reason = "Liability backed by insurance requirement"
            elif any(k in text_lower for k in ["mutual", "reciprocal"]):
                severity = "Low"
                risk_points = 3
                reason = "Mutual limitation of liability detected"
            else:
                severity = "Medium"
                risk_points = 15
                reason = "Limitation of liability warnings"
        elif clause_type == "Termination":
            if any(k in text_lower for k in ["30 days", "30-day", "thirty days", "thirty-day"]):
                severity = "Medium"
                risk_points = 15
                reason = "Standard 30-day termination notice"
            elif any(k in text_lower for k in ["60 days", "60-day", "sixty days", "sixty-day"]):
                severity = "Medium"
                risk_points = 10
                reason = "Standard 60-day termination notice"
            elif any(k in text_lower for k in ["90 days", "90-day", "ninety days", "ninety-day"]):
                severity = "Low"
                risk_points = 3
                reason = "Extended 90-day termination notice"
            elif any(k in text_lower for k in ["immediately", "immediate", "without notice"]):
                severity = "High"
                risk_points = 25
                reason = "Immediate termination risk detected"
            elif any(k in text_lower for k in ["material breach", "for cause", "default"]):
                severity = "Low"
                risk_points = 8
                reason = "Termination for cause / material breach"
            else:
                severity = "Low"
                risk_points = 10
                reason = "Standard termination terms"
        elif clause_type == "Payment Terms":
            if any(k in text_lower for k in ["net 90", "90 days after"]):
                severity = "High"
                risk_points = 15
                reason = "Highly unfavorable Net-90 payment terms"
            elif any(k in text_lower for k in ["net 60", "60 days after"]):
                severity = "Medium"
                risk_points = 10
                reason = "Unfavorable Net-60 payment terms"
            elif any(k in text_lower for k in ["net 30", "30 days after"]):
                severity = "Low"
                risk_points = 5
                reason = "Standard Net-30 payment terms"
            elif any(k in text_lower for k in ["advance", "upfront", "retainer"]):
                severity = "Low"
                risk_points = 2
                reason = "Upfront payment / advance retainer required"
            elif any(k in text_lower for k in ["penalty", "late interest", "interest on late"]):
                severity = "Low"
                risk_points = 1
                reason = "Late payment interest penalty"
            else:
                severity = "Low"
                risk_points = 4
                reason = "Standard payment provisions"
        elif clause_type == "Confidentiality":
            if any(k in text_lower for k in ["perpetual", "indefinite", "survive indefinitely"]):
                severity = "Low"
                risk_points = 3
                reason = "Perpetual confidentiality obligation"
            elif any(k in text_lower for k in ["2 years", "two years", "3 years", "three years"]):
                severity = "Medium"
                risk_points = 8
                reason = "Time-limited confidentiality covenant"
            elif any(k in text_lower for k in ["missing", "no confidentiality"]):
                severity = "High"
                risk_points = 20
                reason = "Missing standard confidentiality protections"
            else:
                severity = "Low"
                risk_points = 5
                reason = "Standard confidentiality protections"
        elif clause_type == "Non-Compete":
            if any(k in text_lower for k in ["worldwide", "global", "any country"]):
                severity = "High"
                risk_points = 20
                reason = "Worldwide non-compete restriction"
            elif any(k in text_lower for k in ["state", "province", "territory"]):
                severity = "Medium"
                risk_points = 8
                reason = "State-wide non-compete restriction"
            elif any(k in text_lower for k in ["6 months", "six months", "1 year", "one year"]):
                severity = "Low"
                risk_points = 5
                reason = "Standard short duration non-compete"
            elif any(k in text_lower for k in ["5 years", "five years", "3 years", "three years"]):
                severity = "High"
                risk_points = 25
                reason = "Extended duration non-compete restriction"
            else:
                severity = "Medium"
                risk_points = 12
                reason = "Standard non-compete covenant"
        elif clause_type == "Assignment":
            if any(k in text_lower for k in ["without consent", "no consent"]):
                severity = "High"
                risk_points = 15
                reason = "Transfer permitted without consent"
            else:
                severity = "Low"
                risk_points = 2
                reason = "Standard assignment constraints"
        elif clause_type == "Indemnity":
            if any(k in text_lower for k in ["mutual", "reciprocal", "each party", "indemnify each other"]):
                severity = "Low"
                risk_points = 10
                reason = "Mutual indemnification clause"
            else:
                severity = "High"
                risk_points = 20
                reason = "One-sided indemnification obligation"
        elif clause_type == "Intellectual Property":
            if any(k in text_lower for k in ["company owns", "employer owns", "work for hire", "transfer of ip", "assigns all right", "sole property", "exclusive property"]):
                severity = "Low"
                risk_points = 2
                reason = "Standard IP assignment to company"
            elif any(k in text_lower for k in ["shared", "joint", "co-own", "jointly"]):
                severity = "Medium"
                risk_points = 10
                reason = "Shared / joint IP ownership"
            else:
                severity = "High"
                risk_points = 20
                reason = "Missing IP assignment provisions"

        return {
            "clause_type": clause_type,
            "confidence": confidence,
            "matched_text": text,
            "reason": reason,
            "severity": severity,
            "risk_points": risk_points
        }
    except Exception as e:
        # Re-raise standard errors if model runtime fails
        raise RuntimeError(f"Classifier prediction runtime error: {e}")

if __name__ == "__main__":
    # Local CLI test
    test_text = "Either party may terminate this agreement with thirty days written notice for convenience."
    print("Testing local prediction:")
    try:
        print(predict_clause(test_text))
    except Exception as ex:
        print(f"Exception: {ex}")