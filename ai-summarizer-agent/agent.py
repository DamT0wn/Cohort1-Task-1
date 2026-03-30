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

        # Allow model overrides via env var for easier rollout/migration.
        model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
    
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
        
        response = self.model.generate_content(prompt)
        summary = response.text.strip()
        
        return summary
