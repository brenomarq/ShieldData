import pandas as pd
import re
from pandas import DataFrame
from validator import Validator

file_path = "data/raw/Hackathon Participa DF Data.xlsx" # Caminho para o arquivo
df: DataFrame = pd.read_excel(file_path, engine="openpyxl", index_col="ID") # Lê o arquivo python 

# Limpa a formatação dos espaços
def safe_clean(text: str) -> str:
    if pd.isna(text) or str(text).strip() == "":
        return ""

    text = str(text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text


df['Texto Mascarado'] = df['Texto Mascarado'].apply(safe_clean) # Aplica a limpeza

# Na preparação do Dataset
df_labels = df['Texto Mascarado'].apply(Validator.validate_all_types).apply(pd.Series)

# Criamos as colunas multi-label para o BERT
df_labels = df_labels.astype(int)
df = df.join(df_labels)

# Verificando a distribuição de cada label
print("Distribuição das labels:")
print(df_labels.sum())

mask = df.duplicated(subset=["Texto Mascarado"], keep="first") # Duplicata removida

removidos = df[mask] # Retorna os dados removidos
df = df[~mask] # Retorna o Dataframe sem o dado duplicado



df.to_excel("data/processed/Hackathon Participa DF Data Processado.xlsx")  # exporta os dados processados para outro arquivo xlsx

print(removidos) # Dados duplicados removidos

print(df)
