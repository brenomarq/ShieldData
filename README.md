# ShieldData

Repositório criado para o Hackathon em Controle Social promovido pelo GDF em 2026.

## Estrutura do Projeto

*   `src/`: Código fonte principal.
    *   `preprocessing.py`: Script CLI para processamento de dados.
    *   `validator.py`: Utilitário para validação de regex (CPF, CNPJ, etc).
    *   `ner_detector.py`: Detector de Entidades Nomeadas usando Spacy.
    *   `score_calculator.py`: Calculadora de métricas.
*   `tests/`: Testes automatizados.
    *   `test_score_calculator.py`: Testes com pytest.
*   `data/`: Diretório de dados (raw/processed).

## Instalação

```bash
pip install -r requirements.txt
python -m spacy download pt_core_news_lg
```

## Uso

### Processamento de Dados

Para processar o arquivo Excel bruto e gerar o arquivo com labels:

```bash
python src/preprocessing.py --input "data/raw/Hackathon Participa DF Data.xlsx" --output "data/processed/Hackathon Participa DF Data Processado.xlsx"
```

## Testes

Para rodar os testes:

```bash
pytest tests/
```
