import json

from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()


def review_code(code, ast_result):

    prompt = f"""
You are an expert Python code reviewer.

Review the following Python code.

CODE:
{code}

STATIC AST ANALYSIS:
{ast_result}

Return ONLY valid JSON using exactly this structure:

{{
    "summary": "Short overall review of the code",
    "bugs": [],
    "performance": [],
    "quality": [],
    "suggestions": []
}}

Rules:
- Return only JSON.
- Do not use Markdown.
- Do not use ```json.
- Do not add text before or after the JSON.
- Each category must contain a list of strings.
- If a category has no findings, return an empty list.
- Do not invent problems.
- Keep findings concise and practical.
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    review_text = response.text.strip()

    # Convert Gemini's JSON text into a Python dictionary
    try:
        review = json.loads(review_text)
    except json.JSONDecodeError:
        # Handle accidental markdown code fences
        if review_text.startswith("```"):
            review_text = review_text.replace("```json", "")
            review_text = review_text.replace("```", "")
            review_text = review_text.strip()

        review = json.loads(review_text)

    return review