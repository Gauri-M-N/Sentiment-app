from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_TITLE: str = "Sentiment API"
    DB_URL: str = "sqlite:///./sentiments.db"
    CORS_ORIGINS: list[str] = ["http://localhost:8501", "http://127.0.0.1:8501"]

settings = Settings()
