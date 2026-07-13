import os
import sys
import unittest
import json

# Append parent directory so the test runner can locate entity_extractor cleanly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from entity_extractor import extract_entities_from_string

class TestNERIntegrationWorkflow(unittest.TestCase):
    """
    Day 18 Automated Unit Testing Suite:
    Validates structural JSON conversion and core extraction function reliability.
    """

    def setUp(self):
        """Define standard layout contract matrices for consistent pipeline verification."""
        self.lease_mock_text = (
            "This LEASE AGREEMENT is entered into on June 15, 2026, by and between "
            "Microsoft Corporation and Wipro Technologies. The monthly rent is $12,500 USD "
            "managed in California."
        )

    def test_json_structure_conversion(self):
        """Verify that the integration function extracts keys as uniform list arrays."""
        extracted_payload = extract_entities_from_string(self.lease_mock_text)
        
        # Test that all core integration entity slots exist
        for entity_key in ["ORG", "DATE", "MONEY", "LOCATION"]:
            self.assertIn(entity_key, extracted_payload)
            self.assertIsInstance(extracted_payload[entity_key], list, f"{entity_key} must convert to a list format!")

    def test_organization_extraction_accuracy(self):
        """Confirm statistical NLP captures specific corporate entities accurately."""
        extracted_payload = extract_entities_from_string(self.lease_mock_text)
        
        self.assertIn("Microsoft Corporation", extracted_payload["ORG"])
        self.assertIn("Wipro Technologies", extracted_payload["ORG"])

    def test_money_normalization_filter(self):
        """Ensure the currency tracking layer captures explicit monetary symbols."""
        extracted_payload = extract_entities_from_string(self.lease_mock_text)
        
        self.assertIn("$12,500 USD", extracted_payload["MONEY"])

if __name__ == "__main__":
    unittest.main()