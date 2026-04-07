def build_review_prompt(code: str, tool_results: dict, parse_result: dict) -> str:
    return (
        "You are a senior code reviewer. Analyze the code and provide logical issues and fixes.\n"
        "Return concise findings.\n\n"
        f"Code:\n{code}\n\n"
        f"Parser summary: {parse_result}\n"
        f"Tool summary: {tool_results}\n"
    )
