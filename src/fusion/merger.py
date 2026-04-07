class ResultMerger:
    def __init__(self, config: dict) -> None:
        self.config = config

    def merge(self, parse_result: dict, tool_results: dict, llm_result: dict, plan: dict) -> dict:
        syntax_issues = parse_result.get("syntax_issues", [])
        lint_issues = tool_results.get("lint", {}).get("lint_issues", [])
        complexity = tool_results.get("complexity", {}).get("complexity")
        if complexity is None:
            complexity = 0

        logic_issues = llm_result.get("logic_issues", [])
        fix_suggestions = llm_result.get("fix_suggestions", [])

        risk_level = self._risk_level(
            syntax_count=len(syntax_issues),
            lint_count=len(lint_issues),
            complexity=int(complexity),
            logic_count=len(logic_issues),
        )

        return {
            "syntax_issues": syntax_issues,
            "lint_issues": lint_issues,
            "logic_issues": logic_issues,
            "complexity": complexity,
            "risk_level": risk_level,
            "fix_suggestions": fix_suggestions,
            "meta": {
                "plan": plan,
                "parse_metrics": parse_result.get("ast_metrics", {}),
                "tool_results": tool_results,
                "llm_mode": llm_result.get("llm_mode", "disabled"),
            },
        }

    @staticmethod
    def _risk_level(syntax_count: int, lint_count: int, complexity: int, logic_count: int) -> str:
        score = syntax_count * 5 + lint_count * 2 + max(complexity - 5, 0) + logic_count * 3
        if score >= 20:
            return "high"
        if score >= 8:
            return "medium"
        return "low"
