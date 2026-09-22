from fastapi import FastAPI
from pydantic import BaseModel

from services.embedding import get_similarity

app = FastAPI()


class SimilarityRequest(BaseModel):
    code1: str
    code2: str


@app.get("/")
def home():
    return {"message": "CodeLens AI backend is running"}


@app.post("/similarity")
def similarity(request: SimilarityRequest):
    score = get_similarity(request.code1, request.code2)

    return {
        "similarity": score
    }