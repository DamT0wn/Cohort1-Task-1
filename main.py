from fastapi import FastAPI, HTTPException, Request
from agent import SummarizerAgent

app = FastAPI()

try:
    agent = SummarizerAgent()
except ValueError as exc:
    print(f"Warning: Agent initialization skipped - {exc}")
    agent = None

@app.get("/")
def root():
    return {"message": "Gemini ADK Agent is running"}

@app.post("/summarize")
async def summarize(request: Request):
    if not agent:
        raise HTTPException(status_code=500, detail="Agent not initialized. Check GEMINI_API_KEY.")

    body = await request.json()
    text = body.get("text", "")

    if not text:
        raise HTTPException(status_code=400, detail="No text provided")

    try:
        summary = agent.summarize_text(text)
        return {
            "input": text,
            "summary": summary
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {exc}")