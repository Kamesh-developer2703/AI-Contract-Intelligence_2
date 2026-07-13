# Model Evaluation Report

Evaluation results on the validation split.

## Summary Metrics

| Metric | Score |
| :--- | :--- |
| **Accuracy** | 0.4106 |
| **Precision (Weighted)** | 0.6390 |
| **Recall (Weighted)** | 0.4106 |
| **F1 Score (Weighted)** | 0.4160 |

## Detailed Classification Report

```text
                   precision    recall  f1-score   support

        Liability       0.74      0.44      0.55        64
      Termination       0.37      0.86      0.52        44
        Indemnity       0.11      0.74      0.18        19
    Governing Law       0.80      0.97      0.88        65
  Confidentiality       0.00      0.00      0.00         0
    Payment Terms       0.21      0.88      0.34        52
       Assignment       0.60      0.43      0.50        74
      Non-Compete       0.25      0.19      0.21        70
General Covenants       0.78      0.22      0.35       401

         accuracy                           0.41       789
        macro avg       0.43      0.53      0.39       789
     weighted avg       0.64      0.41      0.42       789
```
