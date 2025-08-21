import logging
from pathlib import Path
import pandas as pd
import requests

from .config import settings
from .logging_conf import setup_logging
from scripts.generate_synthetic import synthesize  # reuso do gerador

logger = logging.getLogger(__name__)


def ensure_dirs() -> None:
    for p in [settings.RAW_DIR, settings.PROCESSED_DIR, settings.MODELS_DIR, settings.FIGURES_DIR]:
        Path(p).mkdir(parents=True, exist_ok=True)


def download_if_needed() -> Path:
    ensure_dirs()
    raw_path = settings.RAW_DIR / settings.RAW_FILENAME
    if settings.DATA_URL:
        logger.info("Baixando dados de %s ...", settings.DATA_URL)
        r = requests.get(settings.DATA_URL, timeout=60)
        r.raise_for_status()
        raw_path.write_bytes(r.content)
        logger.info("Salvo em %s", raw_path)
    return raw_path


def ensure_raw_dataset() -> Path:
    """Garante um CSV raw: usa local, baixa de URL, ou gera sintético se não houver."""
    raw_path = settings.RAW_DIR / settings.RAW_FILENAME
    if raw_path.exists():
        logger.info("Usando CSV local existente: %s", raw_path)
        return raw_path
    download_if_needed()
    if raw_path.exists():
        return raw_path
    logger.warning("Raw inexistente. Gerando dataset sintético...")
    df = synthesize()
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(raw_path, index=False)
    logger.info("Sintético salvo em %s", raw_path)
    return raw_path


def load_raw(path: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(path, low_memory=False)
    except Exception:
        return pd.read_csv(path, sep=";", low_memory=False)
