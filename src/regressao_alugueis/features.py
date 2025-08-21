import pandas as pd

NUM_COLS = ["quartos", "banheiros", "vagas", "area"]
CAT_COLS = ["bairro", "tipo"]
REQUIRED = ["valor_aluguel"] + NUM_COLS


def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    cols = [c for c in (REQUIRED + CAT_COLS) if c in df.columns]
    out = df[cols].copy()

    for c in NUM_COLS:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce")

    out = out.dropna(subset=[c for c in REQUIRED if c in out.columns])

    if "valor_aluguel" in out.columns:
        q1, q99 = out["valor_aluguel"].quantile([0.01, 0.99])
        out = out[(out["valor_aluguel"] >= q1) & (out["valor_aluguel"] <= q99)]

    return out
