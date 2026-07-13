from .predict import predict_clause

samples = [
    "This agreement shall remain confidential.",
    "Either party may terminate this agreement with thirty days notice.",
    "Payment shall be made within 30 days of invoice.",
    "The supplier shall maintain insurance coverage.",
    "This agreement shall be governed by the laws of India.",
    "Neither party may assign this agreement.",
    "The customer agrees to indemnify the company.",
    "The employee shall not disclose confidential information.",
    "Any dispute shall be resolved through arbitration.",
    "The intellectual property belongs to the company."
]

for i, sample in enumerate(samples, 1):
    print("=" * 60)
    print(f"Test Case {i}")
    print("Input :", sample)
    print("Output:", predict_clause(sample))