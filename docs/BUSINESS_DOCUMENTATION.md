# 📄 BUSINESS_DOCUMENTATION

## 📌 Objetivo do Projeto
Este projeto tem como objetivo prever o valor de aluguel de imóveis em São Paulo com base em características do imóvel (número de quartos, banheiros, vagas, área, bairro, etc.), utilizando dados sintéticos realistas.

---

## ❓ Perguntas de Negócio
1. Quais variáveis mais influenciam o preço do aluguel em São Paulo?  
2. É possível criar um modelo preditivo confiável para estimar os valores de aluguel?  
3. Qual o desempenho dos modelos avaliados em termos de erro e poder explicativo?  
4. Como esse modelo pode apoiar tomadas de decisão estratégicas no mercado imobiliário?  

---

## 📊 Indicadores Utilizados
- Preço do Aluguel (R$) – variável alvo  
- Área útil (m²)  
- Número de quartos, banheiros e vagas  
- Bairro / região  
- Andar  
- Idade do imóvel  

---

## 🔑 Principais Insights
- Área útil e número de quartos foram os fatores com maior impacto direto no preço.  
- Localização (bairro) trouxe forte variabilidade, mostrando que a região é determinante na precificação.  
- O modelo de Regressão Linear apresentou melhor desempenho em termos de erro médio e interpretabilidade.  

---

## 📈 Visualizações Produzidas
- Histogramas dos atributos (área, quartos, banheiros, etc.)  
- Boxplots de preço por bairro  
- Matriz de correlação entre variáveis  
- Dispersões entre preço × área, preço × quartos  

---

## 🏢 Valor para o Negócio
- Suporte para precificação automática de imóveis anunciados.  
- Permite identificar bairros sub ou supervalorizados.  
- Facilita a análise de investimentos em imóveis residenciais.  
- Possibilidade de expandir para outros estados ou países com ajustes mínimos no pipeline.  

---

## 🚀 Próximos Passos de Negócio
- Expandir dataset com dados reais (quando disponíveis).  
- Criar um dashboard interativo para consultas rápidas de preço estimado.  
- Incorporar variáveis externas (ex.: proximidade de metrô, índice de criminalidade).  

---

## 📌 Público-Alvo
- Imobiliárias  
- Corretores de imóveis  
- Investidores  
- Plataformas de aluguel  
