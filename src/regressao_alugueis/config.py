from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Pastas
    DATA_DIR: Path = Path("data")
    RAW_DIR: Path = DATA_DIR / "raw"
    PROCESSED_DIR: Path = DATA_DIR / "processed"
    MODELS_DIR: Path = DATA_DIR / "models"

    DOCS_DIR: Path = Path("docs")
    FIGURES_DIR: Path = DOCS_DIR / "figures"

    # Dados
    RAW_FILENAME: str = "aluguel_sp.csv"
    DATA_URL: Optional[str] = None  # URL opcional para baixar CSV

    # Alvo e split (ATENÇÃO: o nome do alvo é este!)
    TARGET: str = "valor_aluguel"
    TEST_SIZE: float = 0.2
    RANDOM_STATE: int = 42

    # Logging
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
