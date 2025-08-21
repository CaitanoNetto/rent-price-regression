# Previsão de Preços de Aluguéis (Regressão)

Pipeline de ML para prever **valor de aluguel** em SP. Roda 100% por **scripts**:

```bash
# (opcional) gera CSV sintético realista
python -m scripts.generate_synthetic

# processa dados (ou baixa de DATA_URL se configurado) e cria processed/aluguel_clean.csv
python -m scripts.make_dataset

# treina modelos (Linear, RF, XGB), salva melhor pipeline e métricas
python -m scripts.train_model

# gera relatório docs/report.md e figuras docs/figures/
python -m scripts.evaluate_model

# previsão via CLI
python -m scripts.predict_cli --json "{\"quartos\":2,\"banheiros\":1,\"vagas\":1,\"area\":55,\"bairro\":\"Pinheiros\",\"tipo\":\"apto\"}"
Estrutura
src/regressao_alugueis: código do pipeline (config, data, features, model, evaluate)

scripts: entrypoints executáveis

docs: relatório e figuras geradas

tests: testes unitários (pytest)

Dependências
pip install -r requirements.txt
