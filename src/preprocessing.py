import pandas as pd
import re
from typing import Any
from pandas import DataFrame
from validator import Validator
from ner_detector import NamedEntityDetector

file_path = "data/raw/Hackathon Participa DF Data.xlsx" # Caminho para o arquivo
df: DataFrame = pd.read_excel(file_path, engine="openpyxl", index_col="ID") # Lê o arquivo excel

# Limpa a formatação dos espaços
def safe_clean(text: str) -> str:
    if pd.isna(text) or str(text).strip() == "":
        return ""

    text = str(text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def cross_validation(row: "pd.Series[Any]") -> int:
    cols = ["has_cpf", "has_cnpj", "has_email", "has_phone", "has_rg", "has_person_entity"]
    return 1 if any(row[col] == 1 for col in cols) else 0


df['Texto Mascarado'] = df['Texto Mascarado'].apply(safe_clean) # Aplica a limpeza

df_labels = df['Texto Mascarado'].apply(Validator.validate_all_types).apply(pd.Series) # Valida todas as linhas com o Regex

df_labels = df_labels.astype(int) # Converte True or False para inteiros
df = df.join(df_labels) # Adiciona as novas colunas nas labels

ner_detector = NamedEntityDetector()

# 1. Gera os sinais (usando .tolist() para performance)
sinais_list = df['Texto Mascarado'].apply(ner_detector.extract_signals).tolist()

# 2. Cria o DataFrame de colunas extras
df_sinais = pd.DataFrame(sinais_list, index=df.index)

# 3. Join (usando join ou concat)
df = df.join(df_sinais)

# 4. Cross-validation: gera o label final
df['label'] = df.apply(cross_validation, axis=1)

mask = df.duplicated(subset=["Texto Mascarado"], keep="first") # Duplicata removida

removidos = df[mask] # Retorna os dados removidos
df = df[~mask] # Retorna o Dataframe sem o dado duplicado

df.to_excel("data/processed/Hackathon Participa DF Data Processado.xlsx")  # exporta os dados processados para outro arquivo xlsx

print(removidos) # Dados duplicados removidos

print(df)

pd.set_option('display.max_columns', None)
