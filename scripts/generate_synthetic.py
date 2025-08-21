import logging
import numpy as np
import pandas as pd
from src.regressao_alugueis.config import settings
from src.regressao_alugueis.logging_conf import setup_logging

BAIRROS = ["Pinheiros", "Vila Mariana",
           "Moema", "Tatuapé", "Itaim Bibi", "Butantã"]
ROOM_TYPES = ["apto", "casa", "kitnet"]


def synthesize(n=5000, seed=42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    bairros = rng.choice(BAIRROS, size=n, replace=True)
    room_type = rng.choice(ROOM_TYPES, size=n, replace=True)
    quartos = rng.integers(1, 4, size=n)
    banheiros = rng.integers(1, 3, size=n)
    vagas = rng.integers(0, 3, size=n)
    area = rng.normal(60, 20, size=n).clip(20, 180)

    bairro_base = {
        "Pinheiros": 4200, "Vila Mariana": 3800, "Moema": 5000,
        "Tatuapé": 2800, "Itaim Bibi": 5200, "Butantã": 3000
    }
    base = np.array([bairro_base[b] for b in bairros])
    price = base + quartos*700 + banheiros*400 + vagas*300 + (area - 60)*30
    price = price + rng.normal(0, 800, size=n)
    price = price.clip(1000, 20000)

    return pd.DataFrame({
        "bairro": bairros,
        "tipo": room_type,
        "quartos": quartos,
        "banheiros": banheiros,
        "vagas": vagas,
        "area": area.round(1),
        "valor_aluguel": price.round(0).astype(int),
    })


def main():
    setup_logging()
    settings.RAW_DIR.mkdir(parents=True, exist_ok=True)
    df = synthesize()
    out = settings.RAW_DIR / settings.RAW_FILENAME
    df.to_csv(out, index=False)
    logging.info("Dataset sintético salvo em %s (linhas=%d)", out, len(df))


if __name__ == "__main__":
    main()
