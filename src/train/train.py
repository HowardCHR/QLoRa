import argparse
import os
import sys
from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def run_train(config: dict) -> None:
    try:
        from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
    except Exception as e:
        raise RuntimeError("transformers is required for training") from e

    from src.train.collator import CausalLMCollator
    from src.train.dataset import JsonlCodeDataset

    model_cfg = config.get("model", {})
    data_cfg = config.get("data", {})
    train_cfg = config.get("training", {})

    model_path = model_cfg.get("base_model")
    tokenizer_path = model_cfg.get("tokenizer_path") or model_path
    output_dir = model_cfg.get("output_dir", "models/qlora")

    train_ds = JsonlCodeDataset(data_cfg["train_path"])
    val_path = data_cfg.get("val_path")
    eval_ds = JsonlCodeDataset(val_path) if val_path and Path(val_path).exists() else None

    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(model_path)
    collator = CausalLMCollator(tokenizer=tokenizer, max_length=int(data_cfg.get("max_length", 1024)))

    args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=float(train_cfg.get("num_train_epochs", 1)),
        per_device_train_batch_size=int(train_cfg.get("per_device_train_batch_size", 1)),
        gradient_accumulation_steps=int(train_cfg.get("gradient_accumulation_steps", 8)),
        learning_rate=float(train_cfg.get("learning_rate", 2e-4)),
        logging_steps=int(train_cfg.get("logging_steps", 10)),
        save_steps=int(train_cfg.get("save_steps", 200)),
        eval_steps=int(train_cfg.get("eval_steps", 200)),
        warmup_ratio=float(train_cfg.get("warmup_ratio", 0.03)),
        evaluation_strategy="steps" if eval_ds is not None else "no",
        fp16=False,
        bf16=False,
        report_to=[],
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_ds,
        eval_dataset=eval_ds,
        data_collator=collator,
    )
    trainer.train()
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(model_cfg.get("tokenizer_path", output_dir))


def main() -> None:
    parser = argparse.ArgumentParser(description="Train QLoRA model")
    parser.add_argument("--config", default="configs/train.yaml", help="Path to train config")
    args = parser.parse_args()

    config = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
    run_train(config)
    print("Training completed.")


if __name__ == "__main__":
    main()
