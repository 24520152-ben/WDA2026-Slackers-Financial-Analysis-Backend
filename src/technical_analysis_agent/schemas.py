# slackers_trading_agent/src/technical_analysis_agent/schemas.py

from pydantic import BaseModel, Field

class TARequest(BaseModel):
    ticker: str = Field(..., description="Mã cổ phiếu (VD: VCB, FPT, HPG)")
    length: str = Field("3M", description="Khoảng thời gian lấy dữ liệu")

class TAResponse(BaseModel):
    ticker: str = Field(..., description="Mã cổ phiếu (VD: VCB, FPT, HPG)")
    technical_analysis: str = Field(..., description="Phân tích kỹ thuật từ Technical Analysis Agent")