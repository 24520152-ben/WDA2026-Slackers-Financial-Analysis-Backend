# slackers_trading_agent/src/ollama/client.py

import logging
from ollama import Client, ResponseError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, before_sleep_log
from fastapi.concurrency import run_in_threadpool
from src.ollama.config import ollama_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_client = Client(
    host=ollama_settings.HOST,
    headers={'Authorization': f'Bearer {ollama_settings.API_KEY}'}
)

@retry(
    # Thử lại tối đa 3 lần
    stop=stop_after_attempt(3),
    # Chờ đợi tăng dần theo lũy thừa: 2s, 4s, 8s...
    wait=wait_exponential(multiplier=1, min=2, max=10),
    # Chỉ thử lại nếu gặp lỗi từ Server (500, 502, 503...) hoặc lỗi kết nối
    # Không thử lại nếu lỗi 400 (lỗi do mình viết code sai/prompt sai)
    retry=retry_if_exception_type((ResponseError, Exception)),
    # Ghi log trước mỗi lần thử lại để dễ debug
    before_sleep=before_sleep_log(logger, logging.INFO)
)
def _sync_chat_with_retry(messages: list):
    response = _client.chat(
        model=ollama_settings.MODEL,
        messages=messages
    )
    return response['message']['content']

async def call_ollama_cloud(messages: list) -> str:
    report = await run_in_threadpool(_sync_chat_with_retry, messages)
    return report