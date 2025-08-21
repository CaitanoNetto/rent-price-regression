import logging
import pandas as pd
from src.regressao_alugueis.logging_conf import setup_logging
from src.regressao_alugueis.config import settings
from src.regressao_alugueis.data import ensure_raw_dataset, load_raw
from src.regressao_alugueis.features import basic_clean


def main():
    setup_logging()
    logging.info("Criando dataset processado...")
    raw_path = ensure_raw_dataset()
    df_raw = load_raw(raw_path)
    df = basic_clean(df_raw)
    settings.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out = settings.PROCESSED_DIR / "aluguel_clean.csv"
    df.to_csv(out, index=False)
    logging.info("Processado salvo em %s (linhas=%d, colunas=%d)",
                 out, len(df), df.shape[1])


if __name__ == "__main__":
    main()
