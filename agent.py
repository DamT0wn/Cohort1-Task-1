from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel


# Initialize Gemini model
model = GenerativeModel("gemini-1.5-flash")

def summarize_text(text: str) -> str:
    prompt = f"Summarize the following text in 3 concise bullet points:\n\n{text}"
    
    response = model.generate_content(prompt)
    
    return response.text