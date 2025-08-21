import pytest
import pandas as pd
from src.regressao_alugueis.model import build_preprocess, build_models, train_and_select


def test_train_and_select_runs():
    X = pd.DataFrame({
        "num1": [1, 2, 3, 4, 5],
        "cat1": ["a", "b", "a", "b", "a"],
    })
    y = pd.Series([10, 20, 15, 25, 18])

    num_cols = ["num1"]
    cat_cols = ["cat1"]

    preprocess = build_preprocess(num_cols, cat_cols)
    models = build_models()
    name, pipe, metrics = train_and_select(X, y, preprocess, models)

    assert name in models
    assert hasattr(pipe, "predict")
    assert isinstance(metrics, dict)
