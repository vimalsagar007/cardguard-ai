"""CardGuard AI Global Settings"""
import os
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseModel as BaseSettings

from pydantic import ConfigDict, Field

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # GCP Project Settings
    GOOGLE_CLOUD_PROJECT: str = Field(default="cardguard-ai-dev", description="GCP Project ID")
    GOOGLE_CLOUD_LOCATION: str = Field(default="us-central1", description="GCP Region")
    GOOGLE_GENAI_USE_VERTEXAI: bool = Field(default=True, description="Whether to use Vertex AI for Gemini")

    # Models
    GEMINI_MODEL_FAST: str = Field(default="gemini-3.8-flash", description="Fast model for simple classification")
    GEMINI_MODEL_REASONING: str = Field(default="gemini-3.8-pro", description="Reasoning model for complex investigation")
    GEMINI_EMBEDDING_MODEL: str = Field(default="text-embedding-004", description="Embedding model")
    GEMINI_API_KEY: str = Field(default="", description="Gemini API Key for local dev")

    # Storage & DB
    GCS_BUCKET_NAME: str = Field(default="cardguard-knowledge-dev", description="GCS bucket for knowledge docs")
    BIGQUERY_DATASET: str = Field(default="cardguard_fraud_db", description="BigQuery dataset")
    PUBSUB_TOPIC_TRANSACTIONS: str = Field(default="cardguard-transactions-dev", description="PubSub topic")
    PUBSUB_SUBSCRIPTION_TRANSACTIONS: str = Field(default="cardguard-transactions-sub-dev", description="PubSub sub")

    # Application Settings
    ENVIRONMENT: str = Field(default="development", description="Execution environment")
    LOG_LEVEL: str = Field(default="INFO", description="Log level")
    PORT: int = Field(default=8000, description="FastAPI Server Port")
    A2A_PORT: int = Field(default=8001, description="A2A Server Port")
    MCP_PORT: int = Field(default=8002, description="MCP Server Port")

    # Cost tracking (per 1k tokens)
    COST_PER_1K_INPUT_FLASH: float = 0.000075
    COST_PER_1K_OUTPUT_FLASH: float = 0.00030
    COST_PER_1K_INPUT_PRO: float = 0.00125
    COST_PER_1K_OUTPUT_PRO: float = 0.00500

settings = Settings()
