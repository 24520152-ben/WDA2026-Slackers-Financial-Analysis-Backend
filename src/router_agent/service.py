# slackers_trading_agent/src/router_agent/service.py

import json
from src.router_agent.constants import SYSTEM_PROMPT, SMALL_TALK_PROMPT
from src.ollama.client import call_ollama_cloud
from src.investment_analysis_agent.service import get_coordinated_consult

async def extract_intent(user_message: str) -> dict:
    messages = [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': user_message}
    ]
    
    response_text = await call_ollama_cloud(messages)
    
    try:
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        json_str = response_text[start_idx:end_idx]
        return json.loads(json_str)
    except Exception:
        return {"has_ticker": False, "ticker": None, "intent": "Khác"}

async def handle_user_chat(user_message: str) -> dict:
    print(f"Khách hàng: {user_message}")
    
    intent_data = await extract_intent(user_message)
    print(f"LLM hiểu: {intent_data}")
    
    if intent_data.get("has_ticker") and intent_data.get("ticker"):
        ticker = intent_data["ticker"].upper()
        print(f"Kích hoạt Investment Analysis Agent cho mã {ticker}...")
        
        analysis_report = await get_coordinated_consult(ticker, user_message)
        
        return {
            "final_summary": analysis_report["final_summary"],
            "ta_report": analysis_report["ta_report"],
            "fa_report": analysis_report["fa_report"],
            "reply": None
        }
    else:
        print("Không có mã cổ phiếu. Kích hoạt luồng trò chuyện tự do...")
        
        messages = [
            {'role': 'system', 'content': SMALL_TALK_PROMPT},
            {'role': 'user', 'content': user_message}
        ]
        
        general_response = await call_ollama_cloud(messages)
        return {
            "reply": general_response,
            "final_summary": None,
            "ta_report": None,
            "fa_report": None
        }