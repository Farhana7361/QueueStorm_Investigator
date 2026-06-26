from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.models import TicketRequest
from app.analyzer import analyze_ticket
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="QueueStorm Investigator", version="1.0.0")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/analyze-ticket")
async def analyze(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(status_code=400, content={"error": "Invalid JSON body"})

    if not body.get("ticket_id"):
        return JSONResponse(status_code=400, content={"error": "Missing required field: ticket_id"})
    if not body.get("complaint"):
        return JSONResponse(status_code=422, content={"error": "Complaint is empty or missing"})

    try:
        ticket = TicketRequest(**body)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": f"Schema error: {str(e)}"})

    try:
        result = await analyze_ticket(ticket)
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        logger.error(f"Analysis error: {type(e).__name__}")
        return JSONResponse(status_code=500, content={"error": "Internal server error"})
