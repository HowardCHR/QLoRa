class AgentPlanner:
    def __init__(self, config: dict) -> None:
        self.config = config
        agent_cfg = config.get("agent", {})
        self.complexity_threshold = int(agent_cfg.get("complexity_threshold", 10))
        self.enable_llm = bool(agent_cfg.get("enable_llm", True))

    def plan(self, parse_result: dict) -> dict:
        syntax_issues = parse_result.get("syntax_issues", [])
        ast_metrics = parse_result.get("ast_metrics", {})
        quick_complexity = int(ast_metrics.get("branching_nodes", 0))

        tool_sequence = ["ast"]

        if syntax_issues:
            tool_sequence.append("lint")
            return {
                "tool_sequence": tool_sequence,
                "call_llm": False,
                "reason": "syntax_error_detected",
            }

        tool_sequence.extend(["lint", "complexity"])
        call_llm = self.enable_llm and quick_complexity < self.complexity_threshold * 3

        return {
            "tool_sequence": tool_sequence,
            "call_llm": call_llm,
            "reason": "normal_path" if call_llm else "tool_only_path",
        }
