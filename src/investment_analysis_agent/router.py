# slackers_trading_agent/src/investment_analysis_agent/router.py

from fastapi import APIRouter, status
from src.investment_analysis_agent.schemas import ConsultRequest, ConsultResponse
from src.investment_analysis_agent.service import get_coordinated_consult
from src.router_agent.schemas import ChatRequest

router = APIRouter(prefix="/investment_analysis", tags=["Investment Analysis"])

@router.post(
    "/", 
    response_model=ConsultResponse,
    status_code=status.HTTP_200_OK,
    summary="Tư vấn đầu tư tổng hợp tự động bằng LLM",
    description="Manager Agent sẽ điều phối TA và FA Agent chạy song song để đưa ra quyết định cuối cùng."
)
async def investment_consultancy(request: ConsultRequest, user_message: ChatRequest) -> ConsultResponse:
    recommendation = await get_coordinated_consult(request.ticker, user_message.message)
    
    return ConsultResponse(
        ticker=request.ticker,
        investment_analysis=recommendation["final_summary"],
        technical_analysis=recommendation["ta_report"],
        fundamental_analysis=recommendation["fa_report"]
    )