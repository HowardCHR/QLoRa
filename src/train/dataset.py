import json
from pathlib import Path

from torch.utils.data import Dataset


class JsonlCodeDataset(Dataset):
    def __init__(self, path: str) -> None:
        self.samples = []
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Dataset not found: {path}")

        with p.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                self.samples.append(json.loads(line))

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> dict:
        row = self.samples[idx]
        instruction = row.get("instruction", "Review this code")
        input_text = row.get("input", "")
        output_text = row.get("output", "")
        text = f"### Instruction\n{instruction}\n\n### Input\n{input_text}\n\n### Response\n{output_text}"
        return {"text": text}
