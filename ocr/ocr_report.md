# OCR Module Report



# Objective

The objective of the OCR module is to extract readable text from contract PDF documents and provide clean text for downstream NER and clause classification modules.



# Work Completed

### Phase 1 - Environment Setup

* Installed PyMuPDF (fitz)
* Installed pdfplumber
* Installed pytesseract
* Installed Pillow (PIL)
* Installed FastAPI dependencies
* Configured Tesseract OCR

---

### Phase 2 - PDF Text Extraction

Implemented a reusable OCR module capable of:

* Reading digital contract PDFs
* Processing multi-page documents
* Extracting readable text
* Saving extracted text into output files

---

### Phase 3 - OCR Enhancement

Improved the OCR module to support scanned and image-based PDFs.

Implementation includes:

* Automatic detection of pages without selectable text
* Conversion of PDF pages into images
* Text extraction using Tesseract OCR

---

### Phase 4 - Table Extraction

Integrated pdfplumber for table extraction.

Improvements:

* Extracted tables separately
* Cleaned cell formatting
* Replaced multi-line cells with readable text
* Preserved table readability using pipe-separated formatting

---

### Phase 5 - Error Handling

Implemented exception handling for:

* Missing PDF files
* OCR failures
* File saving errors
* Unexpected extraction errors

---

### Phase 6 - Backend Integration

Integrated the OCR module with FastAPI.

Workflow:

Upload PDF
→ Validate file
→ Save uploaded PDF
→ OCR Text Extraction
→ Return extracted text
→ Ready for NER processing

The OCR module was connected with the backend using reusable functions.



# OCR Testing

## Files Tested

* sample_contract.pdf
* sample_employee.pdf
* sample_nda.pdf
* sample_service_agreement.pdf
* sample_lease_agreement.pdf


## Accuracy Observations

* Text extraction was successful for all tested PDFs.
* Paragraph structure remained readable.
* Contract clauses were extracted correctly.
* OCR output was suitable for NER and NLP processing.
* Backend successfully returned extracted text through the API.

---
## Known Limitations

* Complex tables may lose some formatting.
* Low-quality scanned PDFs may reduce OCR accuracy.
* Additional text cleaning may be required for certain document layouts.

---
# Technologies Used

* Python
* PyMuPDF
* pdfplumber
* pytesseract
* Pillow
* FastAPI

---
# Current Status

Completed:

* Digital PDF extraction
* Scanned PDF support
* Image-based PDF support
* Table extraction
* Multi-page PDF processing
* Error handling
* Backend integration
* API testing using Swagger

---
# Conclusion

The OCR module has been successfully implemented and integrated with the backend. It supports both digital and scanned contract PDFs, performs table extraction, and provides clean text for downstream NER and clause classification modules.
