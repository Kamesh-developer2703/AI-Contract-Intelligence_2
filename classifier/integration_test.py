from predict import predict_clause

def test_prediction():

    contract_text = """
    This agreement shall remain confidential.
    Payment shall be made within 30 days.
    Either party may terminate this agreement with written notice.
    """

    result = predict_clause(contract_text)

    print("====== NLP Integration Test ======")
    print("Input:")
    print(contract_text)
    print("\nOutput:")
    print(result)

if __name__ == "__main__":
    test_prediction()