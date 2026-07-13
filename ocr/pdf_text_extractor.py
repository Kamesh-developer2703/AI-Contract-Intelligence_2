import fitz  # PyMuPDF
import pdfplumber
import pytesseract
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
def extract_text_from_pdf(pdf_path):
    try:
        all_text = ""
        # Open fitz once for OCR fallback (pixmap rendering)
        pdf = fitz.open(pdf_path)
        with pdfplumber.open(pdf_path) as plumber_pdf:
            for page_num in range(len(pdf)):
                all_text += f"\n========== PAGE {page_num + 1} ==========\n\n"
                # ---------- Normal Text ----------
                page = plumber_pdf.pages[page_num]
                page_text = page.extract_text()
                text = page_text.strip() if page_text else ""
                if text:
                    all_text += text + "\n\n"
                else:
                    # Fallback to OCR for scanned/image-based pages
                    pix = pdf[page_num].get_pixmap(dpi=300)
                    image = pix.pil_image()
                    ocr_text = pytesseract.image_to_string(image)
                    if ocr_text.strip():
                        all_text += "===== OCR TEXT =====\n"
                        all_text += ocr_text + "\n\n"
                    else:
                        all_text += "No text found on this page.\n\n"
                # ---------- Tables ----------
                tables = plumber_pdf.pages[page_num].extract_tables()
                if tables:
                    all_text += "========== TABLES ==========\n\n"
                    for table in tables:
                        # Determine column count from the row with most cells
                        col_count = max(len(row) for row in table if row)
                        for row in table:
                            if not row:
                                continue
                            # Normalize all cells: replace None with empty string, strip whitespace
                            cleaned = []
                            for cell in row:
                                if cell is None:
                                    cleaned.append("")
                                else:
                                    # Replace newlines inside a cell with a space
                                    cleaned.append(cell.replace("\n", " ").strip())
                            # Pad row to full column count so alignment stays consistent
                            while len(cleaned) < col_count:
                                cleaned.append("")
                            # Skip completely empty rows
                            if not any(cleaned):
                                continue
                            # Format as pipe-separated columns for readability
                            all_text += " | ".join(cleaned) + "\n"
                        all_text += "========== END OF TABLE ==========\n\n"
        page_count = len(pdf)
        pdf.close()
        print(f"Processed {page_count} pages successfully.")
        return all_text
    except FileNotFoundError:
        print(f"Error: File not found -> {pdf_path}")
        return None
    except Exception as e:
        print(f"Error while reading PDF: {e}")
        return None
def save_text_to_file(text, output_path):
    try:
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(text)
        print(f"Saved to: {output_path}")
    except Exception as e:
        print(f"Error while saving file: {e}")
if __name__ == "__main__":
    pdf_path = "ocr/sample_pdfs/sample_employee.pdf"
    output_path = "ocr/outputs/sample_employee.txt"
    extracted_text = extract_text_from_pdf(pdf_path)
    if extracted_text:
        save_text_to_file(extracted_text, output_path)
        print("Text extracted successfully!")
    else:
        print("Text extraction failed.")