from dataclasses import dataclass


@dataclass
class CausalLMCollator:
    tokenizer: object
    max_length: int

    def __call__(self, batch: list[dict]) -> dict:
        texts = [x["text"] for x in batch]
        encoded = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=self.max_length,
            return_tensors="pt",
        )
        encoded["labels"] = encoded["input_ids"].clone()
        return encoded
