# slackers_trading_agent/src/router_agent/router.py

from fastapi import APIRouter, status
from src.router_agent.schemas import ChatRequest, ChatResponse
from src.router_agent.service import handle_user_chat

router = APIRouter(prefix="/chat", tags=["Chat & Routing"])

@router.post(
    "/", 
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Giao tiếp với Trợ lý ảo"
)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    reply_content = await handle_user_chat(request.message)
    return ChatResponse(
        reply=reply_content["reply"],
        investment_analysis=reply_content["final_summary"],
        technical_analysis=reply_content["ta_report"],
        fundamental_analysis=reply_content["fa_report"]
    )