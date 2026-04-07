class BaseTool:
    name = "base"

    def run(self, code: str) -> dict:
        raise NotImplementedError
