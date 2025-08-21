# Relatório — Regressão de Aluguéis

## CV (5-fold)

```json
{
  "linreg": {
    "rmse": 785.2279884350452,
    "mae": 629.1120535714285,
    "r2": 0.6913152987842633
  },
  "rf": {
    "rmse": 864.8567383892911,
    "mae": 691.1895225346884,
    "r2": 0.6255344146670803
  },
  "xgb": {
    "rmse": 871.1298122778495,
    "mae": 697.7811910201092,
    "r2": 0.6200824975967407
  }
}
```

## Teste (hold-out)

```json
{
  "rmse": 799.1678638986791,
  "mae": 643.7256831726152,
  "r2": 0.6873843747340198
}
```

## Figuras

![residuos](docs/figures/residuals.png)

## Top 20 coeficientes (modelo Linear Regression)

| feature                  |        coef |
|:-------------------------|------------:|
| cat__bairro_Tatuapé      | -1152.08    |
| cat__bairro_Itaim Bibi   |  1151.95    |
| cat__bairro_Moema        |   972.058   |
| cat__bairro_Butantã      |  -965.291   |
| num__area                |   551.215   |
| num__quartos             |   550.847   |
| num__vagas               |   226.227   |
| cat__bairro_Vila Mariana |  -206.957   |
| cat__bairro_Pinheiros    |   200.328   |
| num__banheiros           |   195.973   |
| cat__tipo_apto           |   -35.5286  |
| cat__tipo_kitnet         |    30.4173  |
| cat__tipo_casa           |     5.11131 |