import os
import google.generativeai as genai


class SummarizerAgent:
    """Gemini-powered text summarizer with model fallback for reliability."""

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")

        genai.configure(api_key=api_key)
        self.model_candidates = self._build_model_candidates(os.getenv("GEMINI_MODEL"))

    def _build_model_candidates(self, preferred_model: str | None) -> list[str]:
        candidates = []
        static_candidates = [
            preferred_model,
            "gemini-2.5-flash",
            "gemini-2.0-flash",
            "gemini-1.5-flash",
            "gemini-1.5-pro",
        ]

        for model_name in static_candidates:
            if model_name and model_name not in candidates:
                candidates.append(model_name)

        # Add any currently available generateContent models as dynamic fallback.
        try:
            for model in genai.list_models():
                methods = getattr(model, "supported_generation_methods", []) or []
                model_name = (getattr(model, "name", "") or "").replace("models/", "")
                if model_name and "generateContent" in methods and model_name not in candidates:
                    candidates.append(model_name)
        except Exception:
            # Keep static fallbacks when model listing is unavailable.
            pass

        if not candidates:
            raise RuntimeError("No Gemini models available for content generation")

        return candidates

    def summarize_text(self, text: str) -> str:
        if not text or not text.strip():
            raise ValueError("No text provided")

        prompt = f"""Summarize the following text in exactly 2-3 lines. Be concise and capture the main points.

Text to summarize:
{text}

Summary:"""

        last_error = None
        for model_name in self.model_candidates:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                summary = (response.text or "").strip()
                if summary:
                    return summary
            except Exception as exc:
                last_error = exc

        raise RuntimeError(
            "Unable to generate summary with available Gemini models. "
            f"Tried: {', '.join(self.model_candidates)}. Last error: {last_error}"
        )