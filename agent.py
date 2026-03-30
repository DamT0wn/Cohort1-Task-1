import os
import google.generativeai as genai


class SummarizerAgent:
    """Gemini-powered text summarizer with model fallback for reliability."""

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")

        preferred_model = os.getenv("GEMINI_MODEL")
        candidates = [
            preferred_model,
            "gemini-1.5-flash",
            "gemini-1.5-flash-002",
            "gemini-1.5-flash-latest",
            "gemini-2.0-flash",
        ]
        self.model_candidates = []
        for model in candidates:
            if model and model not in self.model_candidates:
                self.model_candidates.append(model)

        genai.configure(api_key=api_key)

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