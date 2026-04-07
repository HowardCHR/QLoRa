from src.llm.model_loader import try_load_generator
from src.llm.prompt import build_review_prompt


class ReviewLLM:
    def __init__(self, config: dict) -> None:
        self.config = config
        self.generator = try_load_generator(config)

    def analyze(self, code: str, tool_results: dict, parse_result: dict) -> dict:
        if self.generator is None:
            # Fallback heuristic output keeps the pipeline usable without model files.
            return {
                "logic_issues": [],
                "fix_suggestions": [
                    "Model is not loaded. Place base model and LoRA weights under models/ and rerun.",
                    "Use tool outputs to prioritize syntax and lint fixes first.",
                ],
                "llm_mode": "fallback",
            }

        prompt = build_review_prompt(code, tool_results, parse_result)
        infer_cfg = self.config.get("inference", {})
        out = self.generator(
            prompt,
            max_new_tokens=int(infer_cfg.get("max_new_tokens", 256)),
            do_sample=bool(infer_cfg.get("do_sample", False)),
            temperature=float(infer_cfg.get("temperature", 0.2)),
            top_p=float(infer_cfg.get("top_p", 0.9)),
        )
        text = out[0].get("generated_text", "")

        return {
            "logic_issues": [],
            "fix_suggestions": [text[-500:]],
            "llm_mode": "model",
        }
