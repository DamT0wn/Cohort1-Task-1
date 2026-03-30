# AI Summarizer Agent

A minimal Google ADK agent powered by Gemini for text summarization, hosted on Google Cloud Run.

## Project Overview

This project implements a single-purpose AI agent that:
- Uses **Google ADK** (Agent Development Kit) for agent infrastructure
- Leverages **Gemini 1.5 Flash** for fast, efficient text summarization
- Exposes REST API endpoints via **FastAPI**
- Runs in a Docker container on **Google Cloud Run**
- Summarizes any input text into 2-3 concise lines

## Architecture

```
Client → Cloud Run Service → FastAPI Endpoint → ADK Agent → Gemini API
```

## Local Development

### Prerequisites
- Python 3.10+
- Google Cloud account with Gemini API enabled
- Gemini API key

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your Gemini API key:
```bash
export GEMINI_API_KEY=your_api_key_here
```

3. Run the application:
```bash
python main.py
```

The service will start on `http://localhost:8080`

## API Endpoints

### Health Check
```
GET /
```
Returns service status.

**Response:**
```json
{
  "status": "healthy",
  "service": "AI Summarizer Agent",
  "version": "1.0.0"
}
```

### Summarize Text
```
POST /summarize
```
Summarizes the provided text using the Gemini-powered ADK agent.

**Request:**
```json
{
  "text": "Your long text to summarize goes here..."
}
```

**Response:**
```json
{
  "input": "Your long text to summarize goes here...",
  "summary": "A concise 2-3 line summary of the input text."
}
```

## Example Usage

### Health Check
```bash
curl http://localhost:8080/
```

### Summarize Text
```bash
curl -X POST http://localhost:8080/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Artificial intelligence is transforming industries by automating complex tasks, improving decision-making processes, and enabling new business models. From healthcare diagnostics to financial forecasting, AI systems are becoming essential tools. However, ethical considerations and responsible deployment remain critical challenges that organizations must address to ensure sustainable and fair AI implementation."
  }'
```

**Expected Output:**
```json
{
  "input": "Artificial intelligence is transforming industries...",
  "summary": "AI is revolutionizing various industries through automation and improved decision-making, but organizations must address ethical considerations for responsible deployment. From healthcare to finance, AI tools are becoming essential while raising important questions about fairness and sustainability."
}
```

## Docker Build & Run

### Build locally
```bash
docker build -t ai-summarizer-agent .
```

### Run locally
```bash
docker run -p 8080:8080 \
  -e GEMINI_API_KEY=your_api_key_here \
  ai-summarizer-agent
```

## Google Cloud Run Deployment

### Prerequisites
- Google Cloud CLI (`gcloud`) installed and configured
- Active Google Cloud project
- Billing enabled on the project

### 1) Configure project and region

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud config set run/region asia-south1
```

### 2) Enable required APIs

```bash
gcloud services enable run.googleapis.com cloudbuild.googleapis.com secretmanager.googleapis.com
```

### 3) Store Gemini API key in Secret Manager (recommended)

```bash
echo -n "YOUR_GEMINI_API_KEY" | gcloud secrets create gemini-api-key --data-file=-
```

If the secret already exists, use:

```bash
echo -n "YOUR_GEMINI_API_KEY" | gcloud secrets versions add gemini-api-key --data-file=-
```

### 4) Deploy to Cloud Run from source

```bash
gcloud run deploy ai-summarizer-agent \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-secrets GEMINI_API_KEY=gemini-api-key:latest \
  --memory 512Mi \
  --timeout 300
```

### 5) Test deployed service

```bash
SERVICE_URL=$(gcloud run services describe ai-summarizer-agent --region asia-south1 --format='value(status.url)')
curl "$SERVICE_URL/"
curl -X POST "$SERVICE_URL/summarize" -H "Content-Type: application/json" -d '{"text":"Cloud Run is a fully managed platform for running containers."}'
```

### Quick alternative (less secure)

```bash
gcloud run deploy ai-summarizer-agent \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

### Alternative Regions
- `us-central1` (USA)
- `europe-west1` (Europe)
- `asia-northeast1` (Tokyo)

### Access the deployed service
```bash
curl https://ai-summarizer-agent-xxxxx-xx.a.run.app/
```

## Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `PORT`: Server port (default: 8080)

### Cloud Run Configuration
- **Memory:** 512 MB (configurable)
- **Timeout:** 300 seconds
- **CPU:** 1 (auto-scaling enabled)
- **Concurrency:** 80 requests per instance

## Project Structure

```
ai-summarizer-agent/
├── .dockerignore    # Excludes unnecessary files from image build context
├── agent.py          # ADK Agent class using Gemini
├── main.py           # FastAPI application
├── requirements.txt  # Python dependencies
├── Dockerfile        # Container configuration
└── README.md         # This file
```

## File Descriptions

### agent.py
Defines the `SummarizerAgent` class:
- Initializes Gemini API with API key from environment
- Implements `run(text)` method for summarization
- Uses gemini-1.5-flash model for fast inference

### main.py
FastAPI application:
- `GET /`: Health check endpoint
- `POST /summarize`: Text summarization endpoint
- Handles request validation and error responses
- Cloud Run ready (listens on PORT 8080)

### requirements.txt
Core dependencies:
- `fastapi`: Web framework
- `uvicorn`: ASGI server
- `google-generativeai`: Gemini API client
- `google-cloud-aiplatform`: GCP AI services
- `pydantic`: Data validation

### Dockerfile
Single-stage Docker build:
- Base image: `python:3.10-slim`
- Installs dependencies
- Copies application code
- Runs the app on Cloud Run's `PORT`

## Troubleshooting

### "GEMINI_API_KEY environment variable not set"
Ensure you've set the environment variable:
```bash
export GEMINI_API_KEY=your_key
```

### Cloud Run deployment fails
Check logs:
```bash
gcloud run logs read ai-summarizer-agent --limit=50
```

### Summarization takes too long
The Gemini API may be rate-limited. Cloud Run scales automatically to handle concurrent requests.

## Monitoring

View logs for your deployed service:
```bash
gcloud run logs read ai-summarizer-agent --tail=20
```

View metrics:
```bash
gcloud monitoring read \
  'resource.type="cloud_run_revision"' \
  --filter='resource.labels.service_name="ai-summarizer-agent"'
```

## Next Steps

- Extend with additional NLP tasks (translation, classification, Q&A)
- Add caching layer (Redis) for repeated queries
- Implement request authentication
- Add structured logging and monitoring
- Set up CI/CD pipeline with Cloud Build

## License

MIT License - Feel free to use and modify

## Support

For issues with Gemini API, visit: https://ai.google.dev/
For Cloud Run documentation: https://cloud.google.com/run/docs
