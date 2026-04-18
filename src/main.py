# slackers_trading_agent/src/main.py

from fastapi import FastAPI
from src.fundamental_analysis_agent.router import router as fundamental_analysis_router
from src.technical_analysis_agent.router import router as technical_analysis_router
from src.investment_analysis_agent.router import router as investment_analysis_router
from src.router_agent.router import router as chat_router

app = FastAPI(
    title="Financial Analysis Backend",
    description="Multi-Agent System for Financial Analysis",
)

app.include_router(fundamental_analysis_router)
app.include_router(technical_analysis_router)
app.include_router(investment_analysis_router)
app.include_router(chat_router)

@app.get("/")
async def root():
    return {"message": "Financial Analysis API is running. Visit /docs for Swagger UI."}