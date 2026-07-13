# API Integration Example

## NLP Module

Backend should call:

```python
from classifier.predict import predict_clause

text = "This agreement shall remain confidential."

result = predict_clause(text)

print(result)
```

## Expected Response

```json
{
    "clause_type": "Governing Law",
    "label": 9,
    "confidence": 0.0315
}
```

## Current Status

- Prediction module working.
- Output format verified.
- Waiting for fine-tuned model for accurate predictions.