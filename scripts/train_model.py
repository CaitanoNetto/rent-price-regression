import json
import logging
import pandas as pd
from sklearn.model_selection import train_test_split

from src.regressao_alugueis.logging_conf import setup_logging
from src.regressao_alugueis.config import settings
from src.regressao_alugueis.model import (
    build_preprocess, build_models, train_and_select, evaluate, save_artifacts
)


def main():
    setup_logging()
    path = settings.PROCESSED_DIR / "aluguel_clean.csv"
    if not path.exists():
        raise FileNotFoundError(
            "Rode 'python -m scripts.make_dataset' primeiro.")
    df = pd.read_csv(path)

    y = df[settings.TARGET]
    X = df.drop(columns=[settings.TARGET])

    num_cols = [c for c in X.columns if X[c].dtype != "object"]
    cat_cols = [c for c in X.columns if X[c].dtype == "object"]

    preprocess = build_preprocess(num_cols, cat_cols)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=settings.TEST_SIZE, random_state=settings.RANDOM_STATE
    )

    models = build_models()
    best_name, best_pipe, cv_metrics = train_and_select(
        X_train, y_train, preprocess, models)
    test_metrics = evaluate(best_pipe, X_test, y_test)
    save_artifacts(best_pipe, cv_metrics, test_metrics, settings.MODELS_DIR)

    logging.info("Melhor modelo: %s", best_name)
    logging.info("CV[%s]: %s", best_name, json.dumps(
        cv_metrics[best_name], indent=2))
    logging.info("TEST: %s", json.dumps(test_metrics, indent=2))


if __name__ == "__main__":
    main()
