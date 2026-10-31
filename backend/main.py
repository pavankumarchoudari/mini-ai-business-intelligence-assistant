from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .database import initialize_database
from .ai_interpreter import interpret_question
from .analytics import run_analytics
from .schemas import QuestionRequest, QuestionResponse

app = FastAPI(title="Mini AI Business Intelligence Assistant", version="1.0.0")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=False,
    allow_methods=["GET", "POST"], allow_headers=["*"]
)

@app.on_event("startup")
def startup():
    initialize_database()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/data-quality")
def data_quality():
    return initialize_database()

@app.post("/ask", response_model=QuestionResponse)
def ask_question(payload: QuestionRequest):
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    interpreted = interpret_question(question)
    if not interpreted:
        raise HTTPException(
            status_code=422,
            detail="I could not map that question to a supported analysis. Try asking about total revenue, top product, monthly trend, top region, or comparing two months."
        )
    try:
        result = run_analytics(
            interpreted["intent"], interpreted.get("month1"), interpreted.get("month2")
        )
        return {
            **result,
            "interpretation_method": interpreted.get("method", "unknown")
        }
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception:
        raise HTTPException(status_code=500, detail="An internal error occurred while processing the question.")
