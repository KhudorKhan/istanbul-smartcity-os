from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from agent.orchestrator import AgentOrchestrator

app = FastAPI(title="Istanbul SmartCity AI Agent Core", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = AgentOrchestrator()

class CitizenQuery(BaseModel):
    message: str
    language: Optional[str] = "ru"
    session_id: Optional[str] = "default"
    history: List[Dict[str, str]] = []
    current_location: Optional[str] = None

class AIActionPayload(BaseModel):
    type: str
    data: Dict[str, Any]

class CitizenResponse(BaseModel):
    message: str
    intent: str
    grounded_source: str
    action: Optional[AIActionPayload] = None
    suggested_replies: List[str] = []


def _fallback_body(language: Optional[str]) -> CitizenResponse:
    is_tr = language == "tr"
    return CitizenResponse(
        message=(
            "Yapay zeka asistanı geçici olarak kullanılamıyor. Lütfen biraz sonra tekrar deneyin."
            if is_tr
            else "ИИ-ассистент временно недоступен. Повторите запрос немного позже."
        ),
        intent="FALLBACK",
        grounded_source="Istanbul SmartCity OS local fallback",
        action=None,
        suggested_replies=[]
    )


@app.get("/")
def health():
    return {"status": "UP", "service": "Istanbul SmartCity Real LLM Agent"}


@app.post("/api/v1/ai/orchestrate", response_model=CitizenResponse)
async def orchestrate_query(query: CitizenQuery):
    try:
        result = await orchestrator.run(
            user_message=query.message,
            language=query.language or "ru",
            history=query.history,
            current_location=query.current_location
        )
        action_payload = None
        if result.get("action"):
            action_payload = AIActionPayload(**result["action"])
        return CitizenResponse(
            message=result.get("message") or _fallback_body(query.language).message,
            intent=result.get("intent") or "FALLBACK",
            grounded_source=result.get("grounded_source") or "Istanbul SmartCity OS local fallback",
            action=action_payload
        )
    except Exception:
        return _fallback_body(query.language)
