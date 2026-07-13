# AI Contract Intelligence Platform Backend

A sophisticated AI-powered contract analysis backend utilizing FastAPI, spaCy, LangChain, and Pinecone to ingest legal documents, run OCR, extract key entities, and classify clause risks.

---

## Onboarding Guide for Teammates

Follow these steps to set up the development environment on your local machine:

### 1. Extract the Project Directory
Extract the contents of the project ZIP file to your workspace.

### 2. Set Up a Virtual Environment
Navigate to the extracted project directory and create a clean Python virtual environment. It is recommended to use Python 3.13:
```bash
# Navigate to the project folder
cd AI-Contract-Intelligence_2-main

# Create the virtual environment
python -m venv leo-venv

# Activate the virtual environment
# On Windows (PowerShell):
.\leo-venv\Scripts\Activate.ps1
# On Windows (CMD):
.\leo-venv\Scripts\activate.bat
# On macOS / Linux:
source leo-venv/bin/activate
```

### 3. Install Dependencies
Ensure your `pip` is updated, then install the required Python libraries:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Download the spaCy Model
Our Named Entity Recognition (NER) module relies on spaCy's pre-trained English model. Download it using:
```bash
python -m spacy download en_core_web_sm
```

### 5. Configure Local Environment Variables
Create a `.env` file in the root of the project (sibling to `requirements.txt`) and add your Pinecone API key and index name:
```env
PINECONE_API_KEY="your-api-key-here"
PINECONE_INDEX="your-index-name-here"
```

### 6. Start the FastAPI Development Server
Run the FastAPI application locally using Uvicorn:
```bash
python -m uvicorn api.main:app --reload
```
Once running, you can access:
* **Interactive API Docs (Swagger UI)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
* **Base API Endpoint**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Project Structure

```text
├── api/
│   ├── __init__.py
│   └── main.py              # FastAPI endpoints (/upload, /analyze, /entities, /classify-clause)
├── classifier/
│   ├── predict.py           # Contract Clause Classification model inference
│   ├── label_mapping.py     # Hardcoded label lookup for development
│   └── label_mapping.json   # Extended 41-label CUAD list
├── ner/
│   ├── entity_extractor.py  # spaCy named entity recognition logic
│   └── tests/               # Automated unit tests for NER pipeline
├── ocr/
│   ├── pdf_text_extractor.py# OCR extraction with PyMuPDF & Tesseract fallback
│   └── sample_pdfs/         # Sample PDF contracts for testing
├── vector_search/
│   ├── pinecone_db.py       # Pinecone vector database client initialization
│   └── semantic_search.py   # Semantic vector search using SentenceTransformers
└── requirements.txt         # Project dependencies
```
