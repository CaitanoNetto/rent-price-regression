import logging
import joblib
import pandas as pd
from src.regressao_alugueis.logging_conf import setup_logging
from src.regressao_alugueis.config import settings
from src.regressao_alugueis.evaluate import plot_residuals, write_report


def main():
    setup_logging()
    model_path = settings.MODELS_DIR / "model.pkl"
    test_metrics_path = settings.MODELS_DIR / "test_metrics.json"
    cv_metrics_path = settings.MODELS_DIR / "cv_metrics.json"
    coef_path = settings.MODELS_DIR / "linreg_coefficients.csv"  # NOVO

    if not (model_path.exists() and test_metrics_path.exists() and cv_metrics_path.exists()):
        raise FileNotFoundError(
            "Treine o modelo antes (scripts/train_model.py).")

    pipe = joblib.load(model_path)
    df = pd.read_csv(settings.PROCESSED_DIR / "aluguel_clean.csv")
    X, y = df.drop(columns=[settings.TARGET]), df[settings.TARGET]
    preds = pipe.predict(X)

    settings.FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    figs = {"residuos": str(plot_residuals(
        y, preds, settings.FIGURES_DIR / "residuals.png"))}

    out_md = settings.DOCS_DIR / "report.md"
    write_report(cv_metrics_path, test_metrics_path,
                 figs, out_md, top_coef_path=coef_path)
    logging.info("Relatório gerado em %s", out_md)


if __name__ == "__main__":
    main()
