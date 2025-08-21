from pathlib import Path
import json
import matplotlib.pyplot as plt
import pandas as pd


def plot_residuals(y_true, y_pred, out: Path) -> Path:
    plt.figure(figsize=(6, 4))
    resid = y_true - y_pred
    plt.scatter(y_pred, resid, alpha=0.5)
    plt.axhline(0, color="black", lw=1)
    plt.xlabel("Predito")
    plt.ylabel("Resíduo")
    out.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    return out


def write_report(
    cv_metrics_path: Path,
    test_metrics_path: Path,
    fig_paths: dict,
    out_md: Path,
    top_coef_path: Path = None,
) -> Path:
    cv = json.loads(cv_metrics_path.read_text(encoding="utf-8"))
    test = json.loads(test_metrics_path.read_text(encoding="utf-8"))
    md = [
        "# Relatório — Regressão de Aluguéis",
        "## CV (5-fold)",
        f"```json\n{json.dumps(cv, indent=2)}\n```",
        "## Teste (hold-out)",
        f"```json\n{json.dumps(test, indent=2)}\n```",
        "## Figuras",
    ]
    for k, v in fig_paths.items():
        md.append(f"![{k}]({Path(v).as_posix()})")

    # NOVO: inclui Top 20 coeficientes se houver arquivo
    if top_coef_path and Path(top_coef_path).exists():
        df = pd.read_csv(top_coef_path)
        top = df.reindex(df["coef"].abs().sort_values(
            ascending=False).index).head(20)
        md.append("## Top 20 coeficientes (modelo Linear Regression)")
        # tabela markdown
        md.append(top.to_markdown(index=False))

    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n\n".join(md), encoding="utf-8")
    return out_md
