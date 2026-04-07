import ast

from src.tools.base_tool import BaseTool


class ComplexityTool(BaseTool):
    name = "complexity"
    BRANCH_NODES = (ast.If, ast.For, ast.While, ast.Try, ast.BoolOp, ast.IfExp, ast.ExceptHandler)

    def run(self, code: str) -> dict:
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {
                "complexity": None,
                "error": f"SyntaxError: {e.msg} (line {e.lineno})",
            }

        branching = 0
        functions = 0
        for node in ast.walk(tree):
            if isinstance(node, self.BRANCH_NODES):
                branching += 1
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions += 1

        complexity = 1 + branching
        return {
            "complexity": complexity,
            "branching_nodes": branching,
            "function_count": functions,
        }
