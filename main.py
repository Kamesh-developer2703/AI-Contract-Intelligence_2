from ocr import extract_text
from ner.entity_extractor import extract_entities
from classifier.predict import predict_clause as classify_clause_model
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
import os
import re
from pydantic import BaseModel
from datetime import datetime

def split_into_paragraphs(text: str) -> list:
    if not text:
        return []
    
    lines = text.split('\n')
    paragraphs = []
    current_paragraph = []
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current_paragraph:
                paragraphs.append(" ".join(current_paragraph))
                current_paragraph = []
            continue
            
        if re.match(r"^=+\s*PAGE\s*\d+\s*=+$", stripped, re.IGNORECASE) or stripped.startswith("--- Page") or stripped.startswith("===") or stripped.startswith("#####"):
            if current_paragraph:
                paragraphs.append(" ".join(current_paragraph))
                current_paragraph = []
            continue
            
        is_new_clause = False
        
        # Numbered clauses
        if re.match(r'^(\d+\.|\d+\)|[a-zA-Z]\.|\*|•|-)\s+', stripped):
            is_new_clause = True
            
        # Section / Article
        elif re.match(r'^(Section|Article|Clause|Sec\.)\s+\d+', stripped, re.IGNORECASE):
            is_new_clause = True
            
        # ALL CAPS headings
        elif stripped.isupper() and len(stripped) < 80:
            is_new_clause = True
            
        # Short Title Case headings like Liability, Payment Terms, Governing Law, Assignment, Confidentiality
        elif (
            len(stripped.split()) <= 6
            and len(stripped) < 80
            and stripped == stripped.title()
        ):
            is_new_clause = True
            
        if is_new_clause and current_paragraph:
            paragraphs.append(" ".join(current_paragraph))
            current_paragraph = [stripped]
        else:
            current_paragraph.append(stripped)
            
    if current_paragraph:
        paragraphs.append(" ".join(current_paragraph))
        
    cleaned_paragraphs = []
    for p in paragraphs:
        cleaned = re.sub(r'\s+', ' ', p).strip()
        if len(cleaned) >= 30:
            cleaned_paragraphs.append(cleaned)
            
    print("\n========== PARAGRAPHS ==========")
    for i, p in enumerate(cleaned_paragraphs):
        print(f"\n[{i}]")
        print(p[:120])
    print("===============================\n")
            
    return cleaned_paragraphs


app = FastAPI(
    title="AI Contract Intelligence API",
    description="Backend API for OCR, NER and Clause Classification",
    version="1.0.0"
)

# 2. PASTE THIS EXACT MIDDLEWARE BLOCK RIGHT HERE:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows any local frontend port (like 3001) to talk to the backend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
def home():
    return {"message": "API Running"}


@app.post("/upload", tags=["Upload"])
async def upload_file(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    contents = await file.read()
    max_size = 5 * 1024 * 1024
    if len(contents) > max_size:
        raise HTTPException(status_code=400, detail="File size exceeds 5 MB limit")

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as f:
        f.write(contents)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "saved_path": file_path
    }


@app.get("/analyze", tags=["Integrated Analysis"])
def analyze_pdf():
    files = os.listdir(UPLOAD_FOLDER)
    pdf_files = [f for f in files if f.endswith(".pdf")]

    if not pdf_files:
        raise HTTPException(status_code=404, detail="No contract files found to analyze")

    latest_pdf = max(pdf_files, key=lambda f: os.path.getmtime(os.path.join(UPLOAD_FOLDER, f)))
    file_path = os.path.join(UPLOAD_FOLDER, latest_pdf)
    
    try:
        # 1. Run Core OCR Engine
        raw_text = extract_text(file_path)
        
        # 2. Run Real Machine Learning NER Core
        entities = extract_entities(raw_text)
        
        # 3. DYNAMIC MACHINE LEARNING RISK ASSESSMENT ENGINE
        risk_score = 0
        breakdown = []
        critical_warnings = []
        classified_clauses = []
        governing_law_found = False
        
        # Split document using robust paragraph splitter
        paragraphs = split_into_paragraphs(raw_text)
        
        print("Paragraph Count =", len(paragraphs))
        for p in paragraphs:
            print("----------------")
            print(p)
            
        for paragraph in paragraphs:
            try:
                # RUN YOUR DEPLOYED ROBERTA MODEL ON EACH CLAUSE
                model_prediction = classify_clause_model(paragraph)
                clause_type = model_prediction.get("clause_type", "Unknown Clause")
                confidence = model_prediction.get("confidence", 0.0)
                severity = model_prediction.get("severity", "Low")
                risk_points = model_prediction.get("risk_points", 0)
                reason = model_prediction.get("reason", "Standard clause")
                
                if clause_type != "Unknown Clause":
                    classified_clauses.append({
                        "clause_type": clause_type,
                        "confidence": confidence,
                        "text": paragraph,
                        "parameters": {}
                    })

                if clause_type == "Governing Law":
                    governing_law_found = True

                if risk_points > 0 and clause_type != "Unknown Clause":
                    risk_score += risk_points
                    
                    # Determine recommendations
                    recommendation = "Review this clause carefully with legal counsel."
                    if clause_type == "Liability":
                        if "unlimited" in paragraph.lower() or "uncapped" in paragraph.lower() or "no limit" in paragraph.lower():
                            recommendation = "Negotiate a liability cap of at least 1x annual contract value."
                        elif "cap" in paragraph.lower() or "capped" in paragraph.lower() or "not exceed" in paragraph.lower():
                            recommendation = "Ensure the liability limit aligns with corporate insurance coverage."
                        else:
                            recommendation = "Negotiate mutual limitation of liability clauses."
                    elif clause_type == "Termination":
                        if "convenience" in paragraph.lower() or "without cause" in paragraph.lower():
                            recommendation = "Ensure mutual termination rights and appropriate notice period (e.g. 30/60 days)."
                        else:
                            recommendation = "Confirm notice periods and cure periods for default."
                    elif clause_type == "Indemnity":
                        recommendation = "Ensure indemnification is mutual and limited to third-party claims."
                    elif clause_type == "Non-Compete":
                        recommendation = "Verify that the restrictive scope (duration, geography) is reasonable and compliant."

                    breakdown.append({
                        "clause": clause_type,
                        "score": risk_points,
                        "reason": reason,
                        "recommendation": recommendation,
                        "severity": severity,
                        "matched_text": paragraph
                    })

                    critical_warnings.append({
                        "type": f"{clause_type.upper()} RISK" if clause_type != "Liability" else "LIABILITY BLOCK",
                        "severity": f"{severity} Risk",
                        "text": f"Model flagged risk: '{paragraph[:60]}...'",
                        "rec": recommendation
                    })
            except Exception as ml_err:
                print("\n==========================")
                print("CLASSIFIER ERROR")
                print(ml_err)
                print("==========================\n")
                raise ml_err

        # Check Governing Law penalty
        raw_text_lower = raw_text.lower()
        if not governing_law_found and not any(k in raw_text_lower for k in ["governing law", "jurisdiction"]):
            risk_score += 25
            rec = "Specify governing law and dispute jurisdiction (e.g., State of Delaware or New York)."
            breakdown.append({
                "clause": "Governing Law",
                "score": 25,
                "reason": "No governing law or dispute resolution clause detected",
                "recommendation": rec,
                "severity": "High",
                "matched_text": ""
            })
            critical_warnings.append({
                "type": "MISSING GOVERNING LAW",
                "severity": "High Risk",
                "text": "No governing law or dispute resolution clause detected.",
                "rec": rec
            })

        # Cap the final risk score
        risk_score = min(max(risk_score, 0), 100)

        # 4. Standard Response Payload Mapping
        return {
            "status": "success",
            "filename": latest_pdf,
            "processed_at": datetime.utcnow().isoformat(),
            "risk_score": risk_score,
            "breakdown": breakdown,
            "warnings": critical_warnings,
            "clauses": classified_clauses,
            "entities": {
                "ORG": entities.get("ORG", []),
                "DATE": entities.get("DATE", []),
                "MONEY": entities.get("MONEY", []),
                "LOCATION": entities.get("LOCATION", [])
            },
            "text": raw_text
        }

    except Exception as e:
        if "Fine-tuned model not found" in str(e):
            raise HTTPException(status_code=503, detail=str(e).strip())
        raise HTTPException(status_code=500, detail=f"Analysis pipeline breakdown: {str(e)}")



# Keep individual fallback routes intact for model legacy checks
@app.get("/entities", tags=["NER"])
def extract_entities_api():
    files = os.listdir(UPLOAD_FOLDER)
    pdf_files = [f for f in files if f.endswith(".pdf")]
    if not pdf_files:
        raise HTTPException(status_code=404, detail="No uploaded PDF found.")
    latest_pdf = max(pdf_files, key=lambda f: os.path.getmtime(os.path.join(UPLOAD_FOLDER, f)))
    pdf_path = os.path.join(UPLOAD_FOLDER, latest_pdf)
    text = extract_text(pdf_path)
    return {"status": "success", "filename": latest_pdf, "entities": extract_entities(text)}

class ClauseRequest(BaseModel):
    text: str

@app.post("/classify-clause", tags=["NLP"])
def classify_clause(request: ClauseRequest):
    try:
        result = classify_clause_model(request.text)
        return {
            "status": "success",
            "nlp_module": "connected",
            "clause_type": result["clause_type"],
            "confidence": result["confidence"],
            "supported_clause_types": ["Confidentiality", "Payment Terms", "Termination", "Liability", "Indemnity", "Non-Compete"],
            "message": "Clause classified successfully"
        }
    except Exception as e:
        if "Fine-tuned model not found" in str(e):
            raise HTTPException(status_code=503, detail=str(e).strip())
        raise HTTPException(status_code=500, detail=f"Clause classification failed: {str(e)}")