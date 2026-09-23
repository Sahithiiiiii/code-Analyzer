from fastapi import FastAPI
from pydantic import BaseModel

from services.embedding import get_similarity
from services.ast_analyzer import analyze_code


app = FastAPI()


class SimilarityRequest(BaseModel):
    code1: str
    code2: str


class AnalyzeRequest(BaseModel):
    code: str


@app.get("/")
def home():
    return {
        "message": "CodeLens AI backend is running"
    }


@app.post("/similarity")
def similarity(request: SimilarityRequest):
    score = get_similarity(request.code1, request.code2)

    return {
        "similarity": score
    }


@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    result = analyze_code(request.code)

    return {
        "analysis": result
    }