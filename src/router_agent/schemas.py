# slackers_trading_agent/src/router_agent/schemas.py

from pydantic import BaseModel, Field
from typing import Optional

class ChatRequest(BaseModel):
    message: str = Field(..., description="Tin nhắn text từ người dùng")

class ChatResponse(BaseModel):
    reply: Optional[str] = Field(None, description="Câu trả lời chung (nếu có)")
    investment_analysis: Optional[str] = Field(None, description="Báo cáo tổng hợp và quyết định từ Investment Analysis Agent")
    technical_analysis: Optional[str] = Field(..., description="Phân tích kỹ thuật từ Technical Analysis Agent")
    fundamental_analysis: Optional[str] = Field(..., description="Phân tích cơ bản từ Fundamental Analysis Agent")