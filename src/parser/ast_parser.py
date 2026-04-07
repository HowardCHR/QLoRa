import ast


class ASTParser:
    def parse(self, code: str) -> dict:
        syntax_issues = []
        ast_metrics = {
            "line_count": len(code.splitlines()),
            "function_count": 0,
            "class_count": 0,
            "branching_nodes": 0,
        }

        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            syntax_issues.append(
                {
                    "type": "SyntaxError",
                    "message": e.msg,
                    "line": e.lineno,
                    "offset": e.offset,
                }
            )
            return {
                "syntax_issues": syntax_issues,
                "ast_metrics": ast_metrics,
            }

        for node in ast.walk(tree): # traversal the tree by DFS
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                ast_metrics["function_count"] += 1
            elif isinstance(node, ast.ClassDef):
                ast_metrics["class_count"] += 1
            elif isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.BoolOp, ast.IfExp)):
                ast_metrics["branching_nodes"] += 1

        return {
            "syntax_issues": syntax_issues,
            "ast_metrics": ast_metrics,
        }
