import argparse
import json
import joblib
import pandas as pd
from src.regressao_alugueis.config import settings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=str, required=True,
                        help='Ex: {"quartos":2,"banheiros":1,"vagas":1,"area":55,"bairro":"Pinheiros","tipo":"apto"}')
    args = parser.parse_args()
    payload = json.loads(args.json)
    df = pd.DataFrame([payload])
    pipe = joblib.load(settings.MODELS_DIR / "model.pkl")
    pred = pipe.predict(df)[0]
    print(json.dumps({"prediction": float(pred)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
