# Backend Integration Example

## Backend Usage

```python
from classifier.predict import predict_clause

text = "This agreement shall remain confidential."

result = predict_clause(text)

print(result)
```

## Output

```json
{
    "clause_type": "Confidentiality",
    "label": 4,
    "confidence": 0.91
}
```

The backend should call `predict_clause(text)` after OCR and NER processing.