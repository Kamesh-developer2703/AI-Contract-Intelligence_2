import os
import json
import re
import spacy

# Initialize spaCy engine globally
nlp = spacy.load("en_core_web_sm")

# Indian State Gazetteer
INDIAN_STATES = {
    "Tamil Nadu", "Andhra Pradesh", "Telangana", "Karnataka", "Kerala",
    "Maharashtra", "Gujarat", "Delhi", "Uttar Pradesh", "West Bengal"
}

def clean_ocr_text(raw_text):
    """Utility: Cleans structural line breaks and messy OCR spacing noise."""
    return " ".join(raw_text.split())


def extract_entities_from_string(text_content):
    """
    Extract named entities from OCR text.
    """
    if not text_content:
        return {
            "ORG": [],
            "DATE": [],
            "MONEY": [],
            "LOCATION": []
        }

    clean_text = re.sub(r'\s+', ' ', text_content).strip()

    extracted_data = {
        "ORG": set(),
        "DATE": set(),
        "MONEY": set(),
        "LOCATION": set()
    }

    # Indian state detection
    for state in INDIAN_STATES:
        if re.search(r'\b' + re.escape(state) + r'\b', clean_text, re.IGNORECASE):
            extracted_data["LOCATION"].add(state)

    doc = nlp(clean_text)

    for ent in doc.ents:

        entity = ent.text.strip().strip(",.;-:")

        if entity == "Tesla Inc":
            entity = "Tesla Inc."

        if ent.label_ == "ORG":
            extracted_data["ORG"].add(entity)

        elif ent.label_ in ["DATE", "TIME"]:
            extracted_data["DATE"].add(entity)

        elif ent.label_ in ["MONEY", "QUANTITY"]:
            extracted_data["MONEY"].add(entity)

        elif ent.label_ in ["GPE", "LOC"]:
            extracted_data["LOCATION"].add(entity)

    money_patterns = [
        r'(?:₹|\$|€|£)\s*\d+(?:,\d+)*(?:\.\d+)?\s*(?:USD|INR)?',
        r'\d+(?:,\d+)*(?:\.\d+)?\s*(?:USD|INR)',
        r'\d+\s*(?:LPA|Lakhs?|Cr|Crores?)\b'
    ]

    for pattern in money_patterns:

        for match in re.findall(pattern, clean_text, re.IGNORECASE):

            value = match.strip().strip(",.;-:")

            if not any(value in item for item in extracted_data["MONEY"]):
                extracted_data["MONEY"].add(value)

    final_orgs = set()

    for org in extracted_data["ORG"]:

        if re.search(r'(?:₹|\$|€|£|INR|USD|\d+\s*LPA)', org, re.IGNORECASE):
            extracted_data["MONEY"].add(org)
        else:
            final_orgs.add(org)

    final_money_list = list(extracted_data["MONEY"])

    filtered_money = []

    for item in final_money_list:

        duplicate = False

        for other in final_money_list:

            if item != other and item in other:
                duplicate = True
                break

        if not duplicate:
            filtered_money.append(item)

    return {
        "ORG": sorted(list(final_orgs)),
        "DATE": sorted(list(extracted_data["DATE"])),
        "MONEY": sorted(filtered_money),
        "LOCATION": sorted(list(extracted_data["LOCATION"]))
    }


def extract_contract_entities(input_filename, output_filename):
    """
    Reads OCR text file and writes extracted entities to JSON.
    """

    if not os.path.exists(input_filename):
        return False

    with open(input_filename, "r", encoding="utf-8") as f:
        raw_content = f.read()

    final_data = extract_entities_from_string(raw_content)

    with open(output_filename, "w", encoding="utf-8") as json_file:
        json.dump(final_data, json_file, indent=4)

    rubric_output = "ner/ner_output.json"

    os.makedirs(os.path.dirname(rubric_output), exist_ok=True)

    with open(rubric_output, "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=4)

    return True


# ===========================
# Backend Integration Wrapper
# ===========================
def extract_entities(text):
    """
    Function used by FastAPI backend.

    Input:
        OCR extracted text (string)

    Output:
        Dictionary of extracted entities
    """
    return extract_entities_from_string(text)


if __name__ == "__main__":

    ocr_input = "ocr/extracted_text.txt"

    output_json = "ner/extracted_contract_data.json"

    if os.path.exists(ocr_input):
        extract_contract_entities(ocr_input, output_json)

    else:
        fallback = "ner/extracted_text.txt"
        extract_contract_entities(fallback, output_json)