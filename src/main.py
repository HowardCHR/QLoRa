import argparse
import json
import os
import sys
from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.agent.agent import ReviewAgent


def load_code(code_file: str | None, code_text: str | None) -> str:
    if code_text:
        return code_text
    if code_file:
        return Path(code_file).read_text(encoding="utf-8")
    raise ValueError("Provide --code-file or --code-text")


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Code Review Agent")
    parser.add_argument("--config", default="configs/inference.yaml", help="Config YAML path")
    parser.add_argument("--code-file", default=None, help="Path to source code file")
    parser.add_argument("--code-text", default=None, help="Inline source code")
    parser.add_argument("--output", default=None, help="Output JSON path")
    args = parser.parse_args()

    config = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
    code = load_code(args.code_file, args.code_text)

    agent = ReviewAgent(config=config)
    report = agent.review(code)

    result = json.dumps(report, ensure_ascii=False, indent=2)
    print(result)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(result, encoding="utf-8")


if __name__ == "__main__":
    main()
