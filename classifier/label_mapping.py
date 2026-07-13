"""
Current label mapping is for development/testing.

To improve prediction accuracy,
replace this mapping with the actual
41 CUAD dataset labels after model fine-tuning.
"""

LABEL_MAPPING = {
    0: "Assignment",
    1: "Audit Rights",
    2: "Cap on Liability",
    3: "Change of Control",
    4: "Confidentiality",
    5: "Termination",
    6: "Payment Terms",
    7: "Insurance",
    8: "Intellectual Property",
    9: "Governing Law",
    10: "Non-Compete"
}

def get_clause_name(label_id):
    return LABEL_MAPPING.get(label_id, "Unknown Clause")