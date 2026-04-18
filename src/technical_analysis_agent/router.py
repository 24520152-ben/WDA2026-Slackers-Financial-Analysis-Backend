# slackers_trading_agent/src/technical_analysis_agent/router.py

from fastapi import APIRouter, status
from src.technical_analysis_agent.schemas import TARequest, TAResponse
from src.technical_analysis_agent.service import get_ta_report

router = APIRouter(prefix="/technical_analysis", tags=["Technical Analysis"])

@router.post(
    "/", 
    response_model=TAResponse,
    status_code=status.HTTP_200_OK,
    summary="Phân tích kỹ thuật tự động bằng LLM"
)
async def analyze_ticker(request: TARequest) -> TAResponse:
    report_content = await get_ta_report(ticker=request.ticker, length=request.length)
    return TAResponse(
        ticker=request.ticker,
        technical_analysis=report_content
    )