import json
from pathlib import Path
from typing import Dict, Tuple
import numpy as np
import pandas as pd
import joblib
from packaging import version
import sklearn

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor


def build_preprocess(num_cols, cat_cols):
    num_t = Pipeline(steps=[("scaler", StandardScaler())])

    # compatibilidade entre versões
    ohe_kwargs = {"handle_unknown": "ignore"}
    if version.parse(sklearn.__version__) >= version.parse("1.2"):
        ohe_kwargs["sparse_output"] = False
    else:
        ohe_kwargs["sparse"] = False

    cat_t = Pipeline(steps=[("ohe", OneHotEncoder(**ohe_kwargs))])

    return ColumnTransformer(
        [("num", num_t, num_cols), ("cat", cat_t, cat_cols)],
        remainder="drop",
    )


def build_models() -> Dict[str, object]:
    return {
        "linreg": LinearRegression(),
        "rf": RandomForestRegressor(n_estimators=300, random_state=42),
        "xgb": XGBRegressor(
            n_estimators=400,
            max_depth=6,
            learning_rate=0.08,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1,
        ),
    }


def _get_feature_names_from_preprocess(preprocess: ColumnTransformer) -> np.ndarray:
    """
    Tenta extrair nomes das features após o ColumnTransformer (robusto a versões).
    """
    # sklearn >= 1.0
    try:
        return preprocess.get_feature_names_out()
    except Exception:
        names = []
        for name, trans, cols in preprocess.transformers_:
            if name == "remainder":
                continue
            # pipelines (num/ cat)
            if hasattr(trans, "named_steps"):
                last_step = list(trans.named_steps.values())[-1]
                if hasattr(last_step, "get_feature_names_out"):
                    # OneHotEncoder
                    try:
                        part = last_step.get_feature_names_out(cols)
                    except Exception:
                        part = np.array(cols, dtype=object)
                else:
                    part = np.array(cols, dtype=object)
            elif hasattr(trans, "get_feature_names_out"):
                try:
                    part = trans.get_feature_names_out(cols)
                except Exception:
                    part = np.array(cols, dtype=object)
            else:
                part = np.array(cols, dtype=object)
            names.extend(list(part))
        return np.array(names, dtype=object)


def export_linear_coefficients(pipe: Pipeline, out_csv: Path) -> Path or None:
    """
    Se o estimador final for LinearRegression, salva coeficientes com nomes de features.
    Retorna o path salvo ou None se não for linear.
    """
    est = pipe.named_steps.get("est")
    if not isinstance(est, LinearRegression):
        return None
    preprocess = pipe.named_steps.get("prep")
    feat_names = _get_feature_names_from_preprocess(preprocess)
    coefs = est.coef_.ravel()
    if len(coefs) != len(feat_names):
        # fallback: numeração se tamanho divergir por alguma razão
        feat_names = np.array(
            [f"feature_{i}" for i in range(len(coefs))], dtype=object)
    df = pd.DataFrame({"feature": feat_names, "coef": coefs})
    df["abs_coef"] = df["coef"].abs()
    df = df.sort_values("abs_coef", ascending=False).drop(columns=["abs_coef"])
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_csv, index=False, encoding="utf-8")
    return out_csv


def train_and_select(X_train, y_train, preprocess, models) -> Tuple[str, Pipeline, Dict[str, dict]]:
    from sklearn.model_selection import cross_val_predict, KFold

    best_name, best_rmse, best_pipe = "", np.inf, None
    metrics: Dict[str, dict] = {}
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    for name, est in models.items():
        pipe = Pipeline([("prep", preprocess), ("est", est)])
        preds = cross_val_predict(pipe, X_train, y_train, cv=cv, n_jobs=-1)
        rmse = mean_squared_error(y_train, preds, squared=False)
        mae = mean_absolute_error(y_train, preds)
        r2 = r2_score(y_train, preds)
        metrics[name] = {"rmse": float(
            rmse), "mae": float(mae), "r2": float(r2)}
        if rmse < best_rmse:
            best_rmse, best_name, best_pipe = rmse, name, pipe
    best_pipe.fit(X_train, y_train)
    return best_name, best_pipe, metrics


def evaluate(pipe: Pipeline, X_test, y_test) -> Dict[str, float]:
    preds = pipe.predict(X_test)
    return {
        "rmse": float(mean_squared_error(y_test, preds, squared=False)),
        "mae": float(mean_absolute_error(y_test, preds)),
        "r2": float(r2_score(y_test, preds)),
    }


def save_artifacts(
    pipe: Pipeline, cv_metrics: Dict[str, dict], test_metrics: Dict[str, float], out_dir: Path
):
    out_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, out_dir / "model.pkl")
    (out_dir / "cv_metrics.json").write_text(json.dumps(cv_metrics, indent=2), encoding="utf-8")
    (out_dir / "test_metrics.json").write_text(json.dumps(test_metrics,
                                                          indent=2), encoding="utf-8")

    # NOVO: exporta coeficientes se o modelo for LinearRegression
    coef_path = out_dir / "linreg_coefficients.csv"
    export_linear_coefficients(pipe, coef_path)
