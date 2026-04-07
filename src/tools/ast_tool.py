import ast

from src.tools.base_tool import BaseTool


class ASTTool(BaseTool):
    name = "ast"

    def run(self, code: str) -> dict:
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {
                "ast_issues": [f"SyntaxError: {e.msg} at line {e.lineno}"],
                "functions": [],
                "classes": [],
                "imports": [],
            }

        functions = []
        classes = []
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append(node.name)
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
            elif isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                imports.append(module)

        return {
            "ast_issues": [],
            "functions": sorted(set(functions)),
            "classes": sorted(set(classes)),
            "imports": sorted(set(imports)),
        }
