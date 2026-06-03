import os
import json
import time
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query, BackgroundTasks, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

from app.rag_engine import RagEngine
from app.ingest import Ingestor
from app.database import (
    init_db, 
    save_conversation, 
    save_feedback, 
    get_recent_conversations, 
    get_stats,
    get_latest_conversation_by_session
)

# Use lifespan context manager for FastAPI startup and shutdown resource management
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup tasks
    init_db()
    
    # Load RAG resources in a background thread to prevent blocking port binding
    import asyncio
    asyncio.create_task(asyncio.to_thread(rag_engine.load_resources))
    
    yield
    # Shutdown tasks
    print("[Shutdown] Cleaning up and releasing RAG resources...")
    rag_engine.close()

app = FastAPI(title="Aurelius Concierge API", version="1.0.0", lifespan=lifespan)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG engine
rag_engine = RagEngine()

# JSON file path for query logging
LOG_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "query_logs.jsonl")

class ChatRequest(BaseModel):
    session_id: str
    message: str
    language: Optional[str] = None # can be 'en', 'hi', 'hinglish'

class ChatResponse(BaseModel):
    response: str
    intent: str
    confidence: float
    sources: List[str]
    retrieval_score: float
    latency_ms: int
    conversation_id: Optional[int] = None

class FeedbackRequest(BaseModel):
    conversation_id: int
    rating: int
    comment: Optional[str] = ""
    session_id: Optional[str] = None # Added for session-aware lookup

def log_to_file_sync(session_id, query, detected_lang, intent, confidence, sources, score, guardrail_triggered, response, latency):
    """Synchronous file logger designed to be run in a background thread."""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "session_id": session_id,
        "query": query,
        "detected_language": detected_lang,
        "intent": intent,
        "confidence": confidence,
        "retrieved_docs": sources,
        "retrieval_scores": [score] if score > 0 else [],
        "guardrail_triggered": guardrail_triggered,
        "response": response,
        "latency_ms": latency
    }
    try:
        with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print(f"Failed to write query log to file: {e}")

@app.get("/")
async def root_endpoint():
    """Friendly root endpoint returning status metadata to prevent 404 confusion."""
    return {
        "status": "healthy",
        "service": "Aurelius Concierge API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "docs_url": "/docs"
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest, background_tasks: BackgroundTasks):
    if not req.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
        
    try:
        # Run standard query pipeline
        res = await rag_engine.query(req.session_id, req.message, override_language=req.language)
        
        # Save to DB
        conv_id = save_conversation(
            session_id=req.session_id,
            user_query=req.message,
            response=res["response"],
            intent=res["intent"],
            confidence=res["confidence"],
            retrieval_score=res["retrieval_score"],
            latency_ms=res["latency_ms"]
        )
        
        # Log to file asynchronously in background thread
        background_tasks.add_task(
            log_to_file_sync,
            session_id=req.session_id,
            query=req.message,
            detected_lang=res["detected_language"],
            intent=res["intent"],
            confidence=res["confidence"],
            sources=res["sources"],
            score=res["retrieval_score"],
            guardrail_triggered=res["guardrail_triggered"],
            response=res["response"],
            latency=res["latency_ms"]
        )
        
        return ChatResponse(
            response=res["response"],
            intent=res["intent"],
            confidence=res["confidence"],
            sources=res["sources"],
            retrieval_score=res["retrieval_score"],
            latency_ms=res["latency_ms"],
            conversation_id=conv_id
        )
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to process chat query.")

@app.get("/api/admin/stats")
async def admin_stats():
    try:
        stats = get_stats()
        return {
            "total_queries": stats["total_queries"],
            "avg_retrieval_score": stats["avg_retrieval_score"],
            "hallucination_rate": stats["hallucination_rate"],
            "satisfaction_avg": stats["satisfaction_avg"],
            "intent_distribution": stats["intent_distribution"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch stats.")

@app.get("/api/admin/queries")
async def admin_queries(limit: int = 50, offset: int = 0):
    try:
        queries = get_recent_conversations(limit, offset)
        return queries
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve recent queries.")

@app.post("/api/feedback")
async def submit_feedback(req: FeedbackRequest):
    if req.rating < 1 or req.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    try:
        conv_id = req.conversation_id
        # Session-aware lookup for dynamic conversation IDs
        if conv_id <= 0:
            if req.session_id:
                conv_id = get_latest_conversation_by_session(req.session_id)
            
            # Global fallback fallback if session lookup yields nothing
            if not conv_id or conv_id <= 0:
                recent = get_recent_conversations(limit=1)
                if recent:
                    conv_id = recent[0]["id"]
                else:
                    raise HTTPException(status_code=400, detail="No conversations found to attach feedback")
                
        save_feedback(conv_id, req.rating, req.comment)
        return {"status": "success", "message": "Feedback submitted successfully"}
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error submitting feedback: {e}")
        raise HTTPException(status_code=500, detail="Failed to submit feedback.")

@app.post("/api/ingest")
async def trigger_ingest():
    try:
        ingestor = Ingestor()
        success = ingestor.ingest_all()
        if success:
            # reload engine index/resources
            rag_engine.load_resources()
            return {"status": "success", "message": "Knowledge base ingested and re-indexed successfully"}
        else:
            raise HTTPException(status_code=500, detail="Ingestion failed. No files processed.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to run ingestion pipeline.")

# Structured error handlers to prevent tracebacks leaking
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    print(f"[Global Error] Unhandled exception occurred: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred."}
    )
