import argparse
import json
from pathlib import Path
from typing import Iterable


def iter_jsonl(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def build_dataset(input_path: Path, output_path: Path, limit: int | None = None) -> int:
    rows = []
    for i, row in enumerate(iter_jsonl(input_path), start=1):
        rows.append(
            {
                "instruction": row.get("instruction", "Review the following code."),
                "input": row.get("input", ""),
                "output": row.get("output", ""),
            }
        )
        if limit is not None and i >= limit:
            break

    write_jsonl(output_path, rows)
    return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build training dataset for QLoRA.")
    parser.add_argument("--input", required=True, help="Input JSONL path")
    parser.add_argument("--output", required=True, help="Output JSONL path")
    parser.add_argument("--limit", type=int, default=None, help="Optional sample limit")
    args = parser.parse_args()

    count = build_dataset(Path(args.input), Path(args.output), args.limit)
    print(f"Built dataset with {count} samples -> {args.output}")


if __name__ == "__main__":
    main()
