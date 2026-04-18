# slackers_trading_agent/src/fundamental_analysis_agent/service.py

import pandas as pd
import yfinance as yf
from fastapi.concurrency import run_in_threadpool

from src.fundamental_analysis_agent.constants import SYSTEM_PROMPT
from src.ollama.client import call_ollama_cloud

def _sync_fetch_fundamentals(ticker: str) -> str:
    try:
        yf_ticker = f"{ticker}.VN"
        stock = yf.Ticker(yf_ticker)
        info = stock.info
        
        if 'trailingPE' not in info and 'forwardPE' not in info and 'priceToBook' not in info:
            return f"Không tìm thấy dữ liệu tài chính hợp lệ cho mã {ticker}."

        fa_data = {
            "Chỉ số": [
                "P/E Hiện tại (Trailing PE)", 
                "P/E Dự phóng (Forward PE)",
                "P/B (Giá/Sổ sách)", 
                "ROE (Lợi nhuận/Vốn chủ) %", 
                "ROA (Lợi nhuận/Tài sản) %", 
                "Biên lợi nhuận ròng %",
                "Tăng trưởng Doanh thu %",
                "Tăng trưởng Lợi nhuận Quý %",
                "Tỷ suất Cổ tức %"
            ],
            "Giá trị Hiện tại": [
                round(info.get("trailingPE", 0), 2) if info.get("trailingPE") else "N/A",
                round(info.get("forwardPE", 0), 2) if info.get("forwardPE") else "N/A",
                round(info.get("priceToBook", 0), 2) if info.get("priceToBook") else "N/A",
                round(info.get("returnOnEquity", 0) * 100, 2) if info.get("returnOnEquity") else "N/A",
                round(info.get("returnOnAssets", 0) * 100, 2) if info.get("returnOnAssets") else "N/A",
                round(info.get("profitMargins", 0) * 100, 2) if info.get("profitMargins") else "N/A",
                round(info.get("revenueGrowth", 0) * 100, 2) if info.get("revenueGrowth") else "N/A",
                round(info.get("earningsQuarterlyGrowth", 0) * 100, 2) if info.get("earningsQuarterlyGrowth") else "N/A",
                round(info.get("dividendYield", 0) * 100, 2) if info.get("dividendYield") else "N/A"
            ]
        }
        
        df = pd.DataFrame(fa_data)
        return df.to_markdown(index=False)
        
    except Exception as e:
        return f"Lỗi khi lấy dữ liệu từ Yahoo Finance: {e}"

async def get_fa_report(ticker: str) -> str:
    markdown_table = await run_in_threadpool(_sync_fetch_fundamentals, ticker)
    
    if "Lỗi" in markdown_table or "Không tìm thấy" in markdown_table:
        return markdown_table
    
    user_prompt = f"""
    Thực hiện đánh giá cơ bản cho mã cổ phiếu: {ticker}
    Dưới đây là các chỉ số tài chính quan trọng hiện tại:

    {markdown_table}

    Hãy phân tích và trình bày báo cáo theo đúng cấu trúc Markdown sau:

    ### I. Đánh giá Định giá (Valuation)
    - (Phân tích P/E và P/B)

    ### II. Hiệu quả Sinh lời & Tăng trưởng
    - (Phân tích ROE, ROA, Biên lợi nhuận)
    - (Phân tích tốc độ tăng trưởng)

    ### III. Sức khỏe Tài chính & Cổ tức
    - (Đánh giá mức độ an toàn và tỷ suất cổ tức)

    ### IV. Kết luận & Khuyến nghị
    - **Trạng thái:** (Tuyệt vời / Tốt / Trung bình / Rủi ro)
    - **Hành động:** (MUA TÍCH LŨY / THEO DÕI / KHÔNG NÊN ĐẦU TƯ - Kèm giải thích ngắn gọn trong 1 câu)
    """
    
    messages = [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': user_prompt},
    ]
    
    report = await call_ollama_cloud(messages)

    start = report.rfind("</think>")
    if start != -1:
        return report[start + 8:]
    return report