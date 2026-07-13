import pdfplumber

pdf_path = "ocr/sample_pdfs/sample_employee.pdf"
output_path = "ocr/cleaned_text.txt"

with pdfplumber.open(pdf_path) as pdf, open(output_path, "w", encoding="utf-8") as output:

    for page_num, page in enumerate(pdf.pages):
        output.write(f"\n--- PAGE {page_num + 1} ---\n")
        tables = page.extract_tables()
        if not tables:
            output.write("No tables found on this page.\n")
        for table in tables:
            for row in table:
                cleaned_row = [cell.replace("\n", " ") if cell else "" for cell in row]
                output.write(" | ".join(cleaned_row) + "\n")
print("Cleaned text saved successfully!")
print(f"Saved to: {output_path}")
