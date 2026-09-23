import ast


class CodeAnalyzer(ast.NodeVisitor):

    def __init__(self):
        self.functions = []
        self.loops = 0
        self.nested_loops = 0
        self.builtin_shadowing = []
        self.bare_exceptions = 0
        self.loop_depth = 0
        self.issues = []

    def visit_FunctionDef(self, node):
        self.functions.append(node.name)
        self.generic_visit(node)

    def visit_For(self, node):
        self.loops += 1

        if self.loop_depth > 0:
            self.nested_loops += 1

            self.issues.append({
                "type": "performance",
                "severity": "medium",
                "message": "Nested loop detected. This may lead to O(n²) time complexity."
            })

        self.loop_depth += 1
        self.generic_visit(node)
        self.loop_depth -= 1

    def visit_While(self, node):
        self.loops += 1

        if self.loop_depth > 0:
            self.nested_loops += 1

            self.issues.append({
                "type": "performance",
                "severity": "medium",
                "message": "Nested loop detected. This may lead to O(n²) time complexity."
            })

        self.loop_depth += 1
        self.generic_visit(node)
        self.loop_depth -= 1

    def visit_Name(self, node):
        builtins = {
            "list",
            "str",
            "dict",
            "set",
            "max",
            "min",
            "sum"
        }

        if node.id in builtins and isinstance(node.ctx, ast.Store):

            if node.id not in self.builtin_shadowing:
                self.builtin_shadowing.append(node.id)

                self.issues.append({
                    "type": "quality",
                    "severity": "low",
                    "message": f"'{node.id}' shadows a Python built-in function or type."
                })

        self.generic_visit(node)

    def visit_ExceptHandler(self, node):

        if node.type is None:
            self.bare_exceptions += 1

            self.issues.append({
                "type": "quality",
                "severity": "medium",
                "message": "Bare except detected. It catches every exception and may hide unexpected errors."
            })

        self.generic_visit(node)


def analyze_code(code):
    try:
        tree = ast.parse(code)
    except SyntaxError as error:
        return {
            "valid": False,
            "error": f"Syntax error: {error}"
        }

    analyzer = CodeAnalyzer()
    analyzer.visit(tree)

    return {
        "valid": True,
        "functions": analyzer.functions,
        "loops": analyzer.loops,
        "nested_loops": analyzer.nested_loops,
        "builtin_shadowing": analyzer.builtin_shadowing,
        "bare_exceptions": analyzer.bare_exceptions,
        "issues": analyzer.issues
    }