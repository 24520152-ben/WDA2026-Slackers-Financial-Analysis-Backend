# slackers_trading_agent/src/fundamental_analysis_agent/schemas.py

from pydantic import BaseModel, Field

class FARequest(BaseModel):
    ticker: str = Field(..., description="Mã cổ phiếu (VD: VCB, FPT, HPG)")

class FAResponse(BaseModel):
    ticker: str = Field(..., description="Mã cổ phiếu (VD: VCB, FPT, HPG)")
    fundamental_analysis: str = Field(..., description="Phân tích cơ bản từ Fundamental Analysis Agent")