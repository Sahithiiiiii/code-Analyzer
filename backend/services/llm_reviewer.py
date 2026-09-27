from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()


def review_code(code, ast_result):

    prompt = f"""
You are an expert Python code reviewer.

Review the following Python code:

CODE:
{code}

STATIC AST ANALYSIS:
{ast_result}

Use the AST analysis as supporting evidence, but also inspect the code yourself.

Return the review using these sections:

Summary:
Bugs:
Performance:
Quality:
Suggestions:

Keep the review concise and practical.
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text