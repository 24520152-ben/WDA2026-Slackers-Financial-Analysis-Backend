# slackers_trading_agent/src/ollama/config.py

from pydantic_settings import BaseSettings

class OllamaConfig(BaseSettings):
    API_KEY: str
    HOST: str
    MODEL: str

    class Config:
        env_prefix = "OLLAMA_"
        env_file = ".env"
        extra = "ignore"

ollama_settings = OllamaConfig() # type: ignore