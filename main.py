from fastapi import FastAPI, Request
from agent import summarize_text

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Gemini ADK Agent is running"}

@app.post("/summarize")
async def summarize(request: Request):
    body = await request.json()
    
    text = body.get("text", "")
    
    if not text:
        return {"error": "No text provided"}
    
    summary = summarize_text(text)
    
    return {
        "input": text,
        "summary": summary
    }