from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from agent import SummarizerAgent

app = FastAPI()

try:
    agent = SummarizerAgent()
except ValueError as exc:
    print(f"Warning: Agent initialization skipped - {exc}")
    agent = None

@app.get("/")
def root():
        return {
                "message": "Gemini ADK Agent is running",
                "playground": "/playground",
                "api": "/summarize"
        }


@app.get("/playground", response_class=HTMLResponse)
def playground():
        return """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Gemini Summarizer Playground</title>
    <style>
        :root {
            --bg: #f3efe7;
            --surface: #fffaf1;
            --ink: #1e1c18;
            --muted: #5f584d;
            --accent: #176b4d;
            --accent-2: #f0b24a;
            --border: #d8ccb7;
        }
        * { box-sizing: border-box; }
        body {
            margin: 0;
            font-family: "Segoe UI", "Trebuchet MS", sans-serif;
            color: var(--ink);
            background: radial-gradient(circle at 10% 10%, #fff7ea 0, #f3efe7 45%, #ece6d9 100%);
            min-height: 100vh;
            display: grid;
            place-items: center;
            padding: 24px;
        }
        .card {
            width: min(900px, 96vw);
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            box-shadow: 0 16px 40px rgba(30, 28, 24, 0.08);
            overflow: hidden;
        }
        .header {
            padding: 20px 22px;
            background: linear-gradient(120deg, #1f7a57 0%, #176b4d 55%, #0f5139 100%);
            color: #fff;
        }
        .header h1 {
            margin: 0;
            font-size: 1.35rem;
            letter-spacing: 0.2px;
        }
        .header p {
            margin: 8px 0 0;
            opacity: 0.92;
        }
        .content {
            padding: 18px;
            display: grid;
            gap: 12px;
        }
        textarea {
            width: 100%;
            min-height: 180px;
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 12px;
            font: inherit;
            resize: vertical;
            background: #fff;
            color: var(--ink);
        }
        .row {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            align-items: center;
        }
        button {
            border: 0;
            border-radius: 10px;
            padding: 10px 14px;
            background: var(--accent);
            color: #fff;
            font-weight: 600;
            cursor: pointer;
        }
        button:hover { filter: brightness(1.05); }
        .clear {
            background: var(--accent-2);
            color: #2c2110;
        }
        .status {
            color: var(--muted);
            font-size: 0.95rem;
            min-height: 1.4em;
        }
        .output {
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 12px;
            min-height: 90px;
            background: #fff;
            white-space: pre-wrap;
            line-height: 1.5;
        }
    </style>
</head>
<body>
    <main class="card">
        <section class="header">
            <h1>Gemini Summarizer Playground</h1>
            <p>Type text and get a concise 2-3 line summary from your Cloud Run service.</p>
        </section>
        <section class="content">
            <textarea id="inputText" placeholder="Paste your paragraph here..."></textarea>
            <div class="row">
                <button id="summarizeBtn">Summarize</button>
                <button id="clearBtn" class="clear">Clear</button>
            </div>
            <div class="status" id="status"></div>
            <div class="output" id="summaryOutput">Your summary will appear here.</div>
        </section>
    </main>

    <script>
        const inputEl = document.getElementById("inputText");
        const statusEl = document.getElementById("status");
        const outputEl = document.getElementById("summaryOutput");
        const summarizeBtn = document.getElementById("summarizeBtn");
        const clearBtn = document.getElementById("clearBtn");

        summarizeBtn.addEventListener("click", async () => {
            const text = inputEl.value.trim();
            if (!text) {
                statusEl.textContent = "Please enter some text first.";
                outputEl.textContent = "";
                return;
            }

            summarizeBtn.disabled = true;
            statusEl.textContent = "Generating summary...";
            outputEl.textContent = "";

            try {
                const res = await fetch("/summarize", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ text })
                });

                const data = await res.json();
                if (!res.ok) {
                    throw new Error(data.detail || "Request failed");
                }

                outputEl.textContent = data.summary || "No summary returned.";
                statusEl.textContent = "Done.";
            } catch (err) {
                statusEl.textContent = "Error while summarizing.";
                outputEl.textContent = err.message;
            } finally {
                summarizeBtn.disabled = false;
            }
        });

        clearBtn.addEventListener("click", () => {
            inputEl.value = "";
            statusEl.textContent = "";
            outputEl.textContent = "Your summary will appear here.";
            inputEl.focus();
        });
    </script>
</body>
</html>
"""

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