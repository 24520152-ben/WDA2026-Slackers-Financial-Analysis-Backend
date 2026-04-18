# slackers_trading_agent/src/investment_analysis_agent/schemas.py

from pydantic import BaseModel, Field

class ConsultRequest(BaseModel):
    ticker: str = Field(..., description="Mã cổ phiếu (VD: VCB, FPT, HPG)")

class ConsultResponse(BaseModel):
    ticker: str = Field(..., description="Mã cổ phiếu (VD: VCB, FPT, HPG)")
    investment_analysis: str = Field(..., description="Báo cáo tổng hợp và quyết định từ Investment Analysis Agent")
    technical_analysis: str = Field(..., description="Phân tích kỹ thuật từ Technical Analysis Agent")
    fundamental_analysis: str = Field(..., description="Phân tích cơ bản từ Fundamental Analysis Agent")