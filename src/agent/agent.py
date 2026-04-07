from src.agent.executor import ToolExecutor
from src.agent.planner import AgentPlanner
from src.fusion.merger import ResultMerger
from src.llm.inference import ReviewLLM
from src.parser.ast_parser import ASTParser
from src.tools.ast_tool import ASTTool
from src.tools.complexity_tool import ComplexityTool
from src.tools.lint_tool import LintTool


class ReviewAgent:
    def __init__(self, config: dict) -> None:
        self.config = config
        self.parser = ASTParser()
        self.tools = {
            "lint": LintTool(),
            "complexity": ComplexityTool(),
            "ast": ASTTool(),
        }
        self.planner = AgentPlanner(config)
        self.executor = ToolExecutor(self.tools)
        self.llm = ReviewLLM(config)
        self.merger = ResultMerger(config)

    def review(self, code: str) -> dict:
        parse_result = self.parser.parse(code)
        plan = self.planner.plan(parse_result)

        tool_results = self.executor.run(code=code, tool_sequence=plan["tool_sequence"])

        llm_result = {}
        if plan["call_llm"]:
            llm_result = self.llm.analyze(code=code, tool_results=tool_results, parse_result=parse_result)

        return self.merger.merge(
            parse_result=parse_result,
            tool_results=tool_results,
            llm_result=llm_result,
            plan=plan,
        )
