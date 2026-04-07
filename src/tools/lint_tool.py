import os
import subprocess
import tempfile

from src.tools.base_tool import BaseTool


class LintTool(BaseTool):
    name = "lint"

    def run(self, code: str) -> dict:
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as tmp:
            tmp.write(code)
            tmp_path = tmp.name

        try:
            cmd = ["flake8", "--max-line-length", "100", tmp_path]
            proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
            issues = []
            for raw in proc.stdout.splitlines():
                if not raw.strip():
                    continue
                issues.append(raw)
            return {
                "lint_issues": issues,
                "exit_code": proc.returncode,
            }
        except FileNotFoundError:
            return {
                "lint_issues": [],
                "warning": "flake8 not installed; lint step skipped",
                "exit_code": 0,
            }
        finally:
            os.remove(tmp_path)
