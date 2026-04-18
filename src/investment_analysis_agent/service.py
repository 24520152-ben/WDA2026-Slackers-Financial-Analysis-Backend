# slackers_trading_agent/src/investment_analysis_agent/service.py

import asyncio
from src.technical_analysis_agent.service import get_ta_report
from src.fundamental_analysis_agent.service import get_fa_report
from src.ollama.client import call_ollama_cloud
from src.investment_analysis_agent.constants import SYSTEM_PROMPT

async def get_coordinated_consult(ticker: str, user_message: str) -> dict:
    ta_report, fa_report = await asyncio.gather(
        get_ta_report(ticker, "3M"),
        get_fa_report(ticker)
    )
    
    user_prompt = f"""
    Khách hàng vừa đặt câu hỏi sau: 
    "{user_message}"

    [BÁO CÁO TỪ CHUYÊN VIÊN KỸ THUẬT - TA CHO MÃ {ticker}]
    {ta_report}

    [BÁO CÁO TỪ CHUYÊN VIÊN CƠ BẢN - FA CHO MÃ {ticker}]
    {fa_report}

    Dựa trên 2 báo cáo trên, hãy trả lời khách hàng theo đúng cấu trúc Markdown sau:

    ### Trả lời trọng tâm
    (Trả lời TRỰC TIẾP và ngắn gọn vào câu hỏi "{user_message}" của khách hàng. Thể hiện sự thấu cảm nếu khách hàng đang lo lắng hoặc fomo).

    ### Góc nhìn Đa chiều mã {ticker}
    - **Về Kỹ thuật (Dòng tiền & Xu hướng):** (Tóm tắt 1-2 câu mấu chốt từ báo cáo TA)
    - **Về Cơ bản (Định giá & Sức khỏe):** (Tóm tắt 1-2 câu mấu chốt từ báo cáo FA)

    ### Kế hoạch Hành động
    - **Khuyến nghị chính:** [MUA / BÁN / NẮM GIỮ / QUAN SÁT]
    - **Vùng giá hành động:** (Xác định vùng giá an toàn để ra quyết định)
    - **Mục tiêu (Target):** (Mức giá kỳ vọng)
    - **Cắt lỗ (Stop-loss):** (Mức giá vi phạm kỷ luật)
    """
    
    messages = [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': user_prompt}
    ]
    
    final_summary = await call_ollama_cloud(messages)

    start = final_summary.rfind("</think>")
    if start != -1:
        final_summary = final_summary[start + 8:]
    
    return {
        "final_summary": final_summary,
        "ta_report": ta_report,
        "fa_report": fa_report
    }