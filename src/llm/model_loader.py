from typing import Any


def try_load_generator(config: dict) -> Any:
    model_cfg = config.get("model", {})
    base_model = model_cfg.get("base_model", "")
    lora_path = model_cfg.get("lora_path", "")

    try:
        from transformers import pipeline
    except Exception:
        return None

    if not base_model:
        return None

    try:
        return pipeline(
            task="text-generation",
            model=lora_path if lora_path else base_model,
            tokenizer=model_cfg.get("tokenizer_path") or None,
            device_map="auto",
        )
    except Exception:
        return None
