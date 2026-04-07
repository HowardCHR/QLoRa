class ToolExecutor:
    def __init__(self, tools: dict) -> None:
        self.tools = tools

    def run(self, code: str, tool_sequence: list[str]) -> dict:
        results = {}
        for tool_name in tool_sequence:
            tool = self.tools.get(tool_name)
            if tool is None:
                results[tool_name] = {"error": f"Unknown tool: {tool_name}"}
                continue
            results[tool_name] = tool.run(code)
        return results
