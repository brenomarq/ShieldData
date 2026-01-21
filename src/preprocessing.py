import pandas as pd
import re
from pandas import DataFrame

file_path = "data/raw/Hackathon Participa DF Data.xlsx" # Caminho para o arquivo
df: DataFrame = pd.read_excel(file_path, engine="openpyxl", index_col="ID") # Lê o arquivo python 

# Limpa a formatação dos espaços
def safe_clean(text: str) -> str:
    if pd.isna(text) or str(text).strip() == "":
        return ""

    text = str(text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text

df['Texto Limpo'] = df['Texto Mascarado'].apply(safe_clean) # Aplica a limpeza

mask = df.duplicated(subset=["Texto Limpo"], keep="first") # Duplicata removida

removidos = df[mask] # Retorna os dados removidos
df = df[~mask] # Retorna o Dataframe sem o dado duplicado

print(removidos) # Dados duplicados removidos

print(df)
