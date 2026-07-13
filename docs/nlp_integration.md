# NLP Integration

## Input

Contract text extracted from OCR.

Example:

"This agreement shall remain confidential."

## Processing

- Tokenization
- RoBERTa Prediction
- Confidence Calculation

## Output

{
    "predicted_label": 12,
    "confidence": 0.87
}

## Integration

Backend endpoint:
/classify-clause

Future Work

- Replace mock classifier with fine-tuned RoBERTa model.
- Return actual legal clause names.