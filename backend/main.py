from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from services.embedding import get_similarity
from services.ast_analyzer import analyze_code
from services.llm_reviewer import review_code


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    # Step 1: Analyze the code using AST
    ast_result = analyze_code(request.code)

    # Stop if the Python code has a syntax error
    if not ast_result["valid"]:
        return {
            "error": ast_result["error"]
        }

    # Step 2: Send code + AST findings to Gemini
    ai_review = review_code(
        request.code,
        ast_result
    )

    # Step 3: Return everything to the client
    return {
        "ast_analysis": ast_result,
        "ai_review": ai_review
    }