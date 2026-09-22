from transformers import AutoModel
from torch.nn.functional import cosine_similarity

from services.tokenizer import tokenizer

model = AutoModel.from_pretrained("bert-base-uncased")


def get_embedding(code):
    inputs = tokenizer(code, return_tensors="pt")

    outputs = model(**inputs)

    embedding = outputs.last_hidden_state.mean(dim=1)

    return embedding


def get_similarity(code1, code2):
    embedding1 = get_embedding(code1)
    embedding2 = get_embedding(code2)

    similarity = cosine_similarity(embedding1, embedding2)

    return similarity.item()