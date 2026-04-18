# slackers_trading_agent/src/technical_analysis_agent/service.py

import pandas as pd
import pandas_ta as ta
from vnstock import Quote
from fastapi.concurrency import run_in_threadpool

from src.technical_analysis_agent.utils import prepare_ta_markdown
from src.technical_analysis_agent.constants import SYSTEM_PROMPT
from src.ollama.client import call_ollama_cloud

def _sync_fetch_and_calculate(ticker: str, length: str) -> pd.DataFrame:
    quote = Quote(symbol=ticker, source="VCI")
    df = quote.history(length=length, interval="1D")
    
    df['RSI'] = ta.rsi(close=df['close'], length=14) # type: ignore
    macd = ta.macd(close=df['close'], fast=12, slow=26, signal=9) # type: ignore
    df = df.join(macd)
    bbands = ta.bbands(close=df['close'], length=20, std=2) # type: ignore
    df = df.join(bbands)
    
    return df

async def get_ta_report(ticker: str, length: str) -> str:
    df = await run_in_threadpool(_sync_fetch_and_calculate, ticker, length)
    
    markdown_table = prepare_ta_markdown(df)
    
    user_prompt = f"""
    Thực hiện phân tích kỹ thuật và đưa ra kế hoạch giao dịch cho mã cổ phiếu: {ticker}
    Dưới đây là dữ liệu 15 phiên gần nhất:

    {markdown_table}

    Hãy trình bày báo cáo theo cấu trúc Markdown sau:

    ### I. Đánh giá Trạng thái Kỹ thuật
    - **Xu hướng & Động lượng:** (Phân tích ngắn gọn MACD và RSI)
    - **Biến động giá:** (Phân tích Bollinger Bands, hiện tượng thắt nút cổ chai hoặc giá bám dải)

    ### II. Các mốc giá quan trọng
    - **Hỗ trợ gần nhất (Support):** (Tìm mức giá thấp hoặc dải BBL gần nhất để làm điểm tựa)
    - **Kháng cự gần nhất (Resistance):** (Tìm đỉnh giá cao hoặc dải BBU gần nhất)

    ### III. Khuyến nghị Giao dịch Thực chiến
    - **Hành động:** (MUA / BÁN / NẮM GIỮ / QUAN SÁT)
    - **Vùng giá hành động:** (Ví dụ: Mua gom quanh vùng giá X - Y)
    - **Mục tiêu chốt lời (Target):** (Mức giá Z - Giải thích ngắn gọn)
    - **Ngưỡng cắt lỗ (Stop-loss):** (Mức giá W - Phá vỡ mức này thì xu hướng hỏng)
    """
    
    messages = [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': user_prompt},
    ]
    
    report = await call_ollama_cloud(messages)
    return report