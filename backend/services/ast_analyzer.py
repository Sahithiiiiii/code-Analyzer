import ast


def analyze_code(code):
    tree = ast.parse(code)

    result = {
        "functions": [],
        "loops": 0,
        "nested_loops": 0,
        "builtin_shadowing": [],
        "bare_exceptions": 0
    }

    loop_depth = 0

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):
            result["functions"].append(node.name)

        elif isinstance(node, (ast.For, ast.While)):
            result["loops"] += 1

            if loop_depth > 0:
                result["nested_loops"] += 1

        elif isinstance(node, ast.Name):
            if node.id in {"list", "str", "dict", "set", "max", "min", "sum"}:
                if isinstance(node.ctx, ast.Store):
                    result["builtin_shadowing"].append(node.id)

        elif isinstance(node, ast.ExceptHandler):
            if node.type is None:
                result["bare_exceptions"] += 1

    return result