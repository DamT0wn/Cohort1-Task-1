"""
FastAPI application for the AI Summarizer Agent
Exposes HTTP endpoints to interact with the Gemini-powered summarization agent
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from agent import SummarizerAgent

app = FastAPI(title="AI Summarizer Agent", version="1.0.0")

# Initialize the agent on startup
try:
    agent = SummarizerAgent()
except ValueError as e:
    print(f"Warning: Agent initialization skipped - {e}")
    agent = None


class SummarizeRequest(BaseModel):
    """Request schema for summarization endpoint"""
    text: str


class SummarizeResponse(BaseModel):
    """Response schema for summarization endpoint"""
    input: str
    summary: str


@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Summarizer Agent",
        "version": "1.0.0"
    }


@app.post("/summarize", response_model=SummarizeResponse)
async def summarize(request: SummarizeRequest):
    """
    Summarize the provided text using the Gemini-powered ADK agent
    
    Args:
        request: SummarizeRequest with 'text' field
        
    Returns:
        SummarizeResponse with input and summary
    """
    if not agent:
        raise HTTPException(
            status_code=500,
            detail="Agent not initialized. Check GEMINI_API_KEY environment variable."
        )
    
    try:
        summary = agent.run(request.text)
        
        return SummarizeResponse(
            input=request.text,
            summary=summary
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
