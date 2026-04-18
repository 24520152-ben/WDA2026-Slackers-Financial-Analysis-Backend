# slackers_trading_agent/src/fundamental_analysis_agent/router.py

from fastapi import APIRouter, status
from src.fundamental_analysis_agent.schemas import FARequest, FAResponse
from src.fundamental_analysis_agent.service import get_fa_report

router = APIRouter(prefix="/fundamental_analysis", tags=["Fundamental Analysis"])

@router.post(
    "/", 
    response_model=FAResponse,
    status_code=status.HTTP_200_OK,
    summary="Phân tích cơ bản tự động bằng LLM"
)
async def analyze_fundamentals(request: FARequest) -> FAResponse:
    report_content = await get_fa_report(ticker=request.ticker)
    
    return FAResponse(
        ticker=request.ticker,
        fundamental_analysis=report_content
    )