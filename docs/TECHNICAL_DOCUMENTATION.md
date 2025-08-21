# 📄 TECHNICAL_DOCUMENTATION

## 📌 Visão Geral
Este projeto constrói um pipeline reprodutível de Machine Learning para prever preços de aluguel em São Paulo a partir de dados sintéticos. Abrange desde geração de dados, pré-processamento, treinamento de modelos, avaliação e relatórios.

---

## 🏗️ Arquitetura do Projeto
02-rent-price-regression/
│── data/ <- dados brutos e processados
│── notebooks/ <- notebooks exploratórios
│── scripts/ <- scripts executáveis
│ ├── generate_synthetic.py
│ ├── train_model.py
│ └── evaluate_model.py
│── src/regressao_alugueis/ <- código fonte principal
│ ├── data.py
│ ├── model.py
│ ├── evaluate.py
│ └── utils.py
│── docs/
│ ├── BUSINESS_DOCUMENTATION.md
│ ├── TECHNICAL_DOCUMENTATION.md
│ └── report.md
│── requirements.txt
│── README.md

yaml
Copiar
Editar

---

## ⚙️ Tecnologias Utilizadas
- Python 3.9+  
- Bibliotecas principais:  
  - pandas, numpy → manipulação de dados  
  - scikit-learn → pré-processamento, treino e avaliação de modelos  
  - matplotlib, seaborn → visualizações  
  - logging → rastreamento de execução  
  - pytest → testes unitários  
  - tabulate → formatação de relatórios  

---

## 🚀 Fluxo de Execução
1. **Geração de dados sintéticos**  
   - Script `scripts/generate_synthetic.py` cria dataset com 5.000 registros.  
   - Salvo em `data/raw/aluguel_sp.csv`.  

2. **Treinamento de Modelos**  
   - `scripts/train_model.py` divide dados em treino/teste.  
   - Pré-processamento: OneHotEncoder para categóricas, StandardScaler para numéricas.  
   - Modelos avaliados:  
     - Regressão Linear  
     - Random Forest  
   - Salva melhor modelo em `models/`.  

3. **Avaliação**  
   - `scripts/evaluate_model.py` compara métricas de treino/teste:  
     - RMSE  
     - MAE  
     - R²  
   - Gera relatório `.md` em `docs/report.md`.  

4. **Exploração Interativa**  
   - Notebook `notebooks/01_eda_rent.ipynb` permite análise de distribuições, correlações e resultados.  

---

## 🧪 Testes
- Localizados em `tests/`  
- Validação de funções de pré-processamento e métricas.  
- Execução via `pytest` garante reprodutibilidade.  

---

## 📈 Métricas Obtidas
- Melhor modelo: **Regressão Linear**  
- Resultados em teste:  
  - RMSE ≈ 799  
  - MAE ≈ 643  
  - R² ≈ 0.68  

---

## 📦 Saídas do Projeto
- Modelo treinado em `models/`  
- Relatório de avaliação em `docs/report.md`  
- Dataset processado em `data/processed/`  

---