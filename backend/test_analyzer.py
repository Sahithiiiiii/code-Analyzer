from services.ast_analyzer import analyze_code


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


result = analyze_code(code)

print(result)
