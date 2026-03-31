"""
SummarizerAgent - Google ADK Agent for Text Summarization
Uses Gemini API for inference
"""

import os
import google.generativeai as genai


class SummarizerAgent:
    """
    An ADK agent that uses Gemini to summarize text.
    """
    
    def __init__(self):
        """Initialize the agent with Gemini API key from environment."""
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
    
    def run(self, text: str) -> str:
        """
        Summarize the input text in 2-3 lines.
        
        Args:
            text: The input text to summarize
            
        Returns:
            A summary of the input text (2-3 lines)
        """
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty")
        
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
            except Exception as e:
                last_error = e

        raise RuntimeError(
            "Unable to generate summary with available Gemini models. "
            f"Tried: {', '.join(self.model_candidates)}. Last error: {last_error}"
        )
