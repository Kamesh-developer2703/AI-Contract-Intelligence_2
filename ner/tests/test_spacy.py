import spacy

# 1. Load the pre-trained English brain we downloaded
nlp = spacy.load("en_core_web_sm")

# 2. Define a sample legal sentence to test
#text extracted from output of ocr  for testing purposes
sample_text = """

--- Page 1 ---
 
 
Production-Level Data Science & 
Machine Learning Project Plans 
Project 1: AI-Powered Contract Intelligence & Risk 
Scoring (NLP) 
Project Information 
A sophisticated NLP platform designed for legal and compliance teams. This system ingests 
lengthy legal contracts (PDFs/Word docs), automatically extracts key entities (dates, parties, 
jurisdictions), identifies specific clauses (e.g., termination, confidentiality), and flags 
anomalous or high-risk language using a fine-tuned Large Language Model (LLM) and 
Named Entity Recognition (NER). 
Data Source 
●​ Primary Source: CUAD (Contract Understanding Atticus Dataset). 
●​ Characteristics: A highly specialized dataset comprising over 500 commercial 
contracts with dense legal language, expertly annotated with 41 distinct legal 
categories. 
Tech Stack 
●​ Languages: Python. 
●​ NLP & ML: Hugging Face Transformers (BERT/RoBERTa), spaCy, PyTorch. 
●​ Information Retrieval: Pinecone or Milvus (Vector Database), LangChain. 
●​ Backend/API: FastAPI, Uvicorn, Celery (for asynchronous document processing). 
●​ Deployment: Docker, AWS EC2. 
Expected Impact 
Drastically reduces the manual hours required for legal due diligence and contract review. 
Mitigates business risk by ensuring compliance teams never miss hidden liability clauses or 
unfavorable auto-renewal terms in high-volume contract environments. 
4-Week Development Timeline 
●​ Week 1: Data Parsing & Baseline Modeling 
○​ Day 1-2: Setup environment and process the CUAD dataset into 
training-ready formats (JSON/Tokenized text). 
○​ Day 3-5: Implement OCR pipeline (Tesseract/pdf2image) to handle raw PDF 
ingestion. 
ZAALIMA DEVELOPMENT CONFIDENTIAL 
1 


 
ZAALIMA DEVELOPMENT CONFIDENTIAL 
5 

"""

print("⏳ Processing text with spaCy...")
# 3. Pass the text through the spaCy NLP pipeline
doc = nlp(sample_text)

print("\n🎯 Extracted Entities:")
print("-" * 40)

# 4. Loop through the entities that spaCy's AI discovered
for ent in doc.ents:
    print(f"🔹 Entity: {ent.text:<18} | Label: {ent.label_:<10} | Description: {spacy.explain(ent.label_)}")

print("-" * 40)
#testing complete 