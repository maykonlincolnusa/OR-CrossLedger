# OR CrossLedger

Protótipo para normalizar e correlacionar movimentações provenientes de diferentes ledgers ou instituições, preservando origem e qualidade do dado.

## MVP

- Converter dois formatos CSV para um modelo canônico.
- Conciliar transferências por identificador, valor, moeda e janela temporal.
- Sinalizar divergências, duplicidades e correspondências incertas.
- Rastrear a origem de cada campo normalizado.

## Próximo passo

O pacote já reconcilia pagamentos por valor, moeda e proximidade temporal, preservando itens não conciliados. Próximo: adicionar adaptadores ISO 20022 e métricas de falsos matches.

