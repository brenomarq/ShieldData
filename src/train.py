from piiclassifier import PIIClassifier, PIIDataset, train_epoch
from pandas import DataFrame
from torch.utils.data import DataLoader
import pandas as pd
import torch

file_path = "data/processed/Hackathon Participa DF Data Processado.xlsx" # Caminho para o arquivo
df: DataFrame = pd.read_excel(file_path, engine="openpyxl", index_col="ID") # Lê o arquivo excel

labels_list: list[int] = df["label"].tolist() # Lista de 0s e 1s
texts_list = df["Texto Mascarado"].astype(str).tolist() # Lista de strings

dataset: PIIDataset = PIIDataset(texts_list, labels_list)
data_loader = DataLoader(dataset, batch_size=16, shuffle=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = PIIClassifier()
model = model.to(device)

loss_fn = torch.nn.CrossEntropyLoss() # Função para calcular o erro
optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5) #Otimizador dos pesos AdamW com learning rate de 0.00002

for epoch in range(3):
    print(f"Iniciando época {epoch + 1}...")
    
    acc, loss = train_epoch(
        model= model,
        data_loader= data_loader,
        loss_fn= loss_fn,
        optimizer= optimizer,
        device= device,
        n_examples= len(texts_list)
    )

    print(f"Época {epoch+1} -> Acurácia: {acc}% | Erro: {loss}")

model.save("models")

