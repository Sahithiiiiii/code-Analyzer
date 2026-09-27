from services.ast_analyzer import analyze_code
from services.llm_reviewer import review_code


code = """
def process(data):
    for i in data:
        for j in data:
            print(i, j)

    list = [1, 2, 3]

    try:
        x = 10 / 0
    except:
        pass
"""


ast_result = analyze_code(code)

review = review_code(code, ast_result)

print("\n===== CODE REVIEW =====\n")
print(review)