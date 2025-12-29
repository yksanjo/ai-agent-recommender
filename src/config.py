"""
Configuration management for the AI Agent Recommender.
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # OpenAI
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4-turbo-preview"
    
    # ChromaDB
    chroma_persist_dir: str = "./data/embeddings"
    chroma_collection_name: str = "use_cases"
    
    # Data paths
    use_cases_file: str = "data/use_cases.json"
    processed_use_cases_file: str = "data/use_cases_processed.json"
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_url: Optional[str] = None
    
    # Retriever
    default_k: int = 5
    score_threshold: float = 0.7
    
    # Agent
    agent_temperature: float = 0.7
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()

