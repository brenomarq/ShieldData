import pandas as pd

file_path = "../Hackathon Participa DF Data.xlsx"
df = pd.read_excel(file_path, engine="openpyxl", index_col="ID") 

print(df)

