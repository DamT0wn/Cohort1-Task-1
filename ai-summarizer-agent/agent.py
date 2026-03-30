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

        preferred_model = os.getenv("GEMINI_MODEL")
        self.model_candidates = [
            preferred_model,
            "gemini-1.5-flash",
            "gemini-1.5-flash-002",
            "gemini-1.5-flash-latest",
            "gemini-2.0-flash",
        ]
        # Remove empty values and deduplicate while preserving order.
        self.model_candidates = [m for i, m in enumerate(self.model_candidates) if m and m not in self.model_candidates[:i]]

        genai.configure(api_key=api_key)
    
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
