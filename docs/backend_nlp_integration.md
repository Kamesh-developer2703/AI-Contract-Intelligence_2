# Backend NLP Integration

## Module

Contract Clause Classification

## Function

```python
from classifier.predict import predict_clause
```

## Example

```python
text = "This agreement shall remain confidential."

result = predict_clause(text)
```

## Response

```json
{
  "clause_type": "Governing Law",
  "label": 9,
  "confidence": 0.0315
}
```

## Integration

The backend should replace the current mock response inside `/classify-clause` with:

```python
result = predict_clause(request.text)
return result
```

## Current Limitation

The current model uses the base RoBERTa checkpoint. Accurate legal clause prediction requires a fine-tuned CUAD model.