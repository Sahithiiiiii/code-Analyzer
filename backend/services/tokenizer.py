from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")


def tokenize_code(code):
    return tokenizer.tokenize(code)


def encode_code(code):
    return tokenizer(code, return_tensors="pt")