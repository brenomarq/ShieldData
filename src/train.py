from piiclassifier import PIIClassifier, PIIDataset, train_epoch
from pandas import DataFrame
from torch.utils.data import DataLoader
import pandas as pd
import torch
import os

class ModelTrainer:
    def __init__(
        self,
        data_path: str,
        model_save_path: str = "models",
        batch_size: int = 16,
        learning_rate: float = 2e-5,
        epochs: int = 3,
        model_name: str = "neuralmind/bert-base-portuguese-cased",
        device: str | None = None
    ):
        """
        Classe para gerenciar o treinamento do modelo PIIClassifier.
        
        Args:
            data_path (str): Caminho para o arquivo Excel processado.
            model_save_path (str): Diretório onde o modelo treinado será salvo.
            batch_size (int): Tamanho do lote para treinamento.
            learning_rate (float): Taxa de aprendizado para o otimizador AdamW.
            epochs (int): Número de épocas de treinamento.
            model_name (str): Nome do modelo base BERT a ser utilizado.
            device (str): Dispositivo para treino ('cuda', 'mps' ou 'cpu'). Se None, detecta automaticamente.
        """
        self.data_path = data_path
        self.model_save_path = model_save_path
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.model_name = model_name
        
        if device:
            self.device = torch.device(device)
        else:
            # Tenta detectar CUDA ou MPS , senão fallback para CPU
            if torch.cuda.is_available():
                self.device = torch.device("cuda")
            elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                self.device = torch.device("mps")
            else:
                self.device = torch.device("cpu")
        
        self.model = None
        self.data_loader = None
        self.optimizer = None
        self.loss_fn = torch.nn.CrossEntropyLoss()
        self.dataset_size = 0

    def load_data(self):
        """Carrega os dados do arquivo Excel e prepara o DataLoader."""
        if not os.path.exists(self.data_path):
             raise FileNotFoundError(f"Arquivo não encontrado: {self.data_path}")


        df: DataFrame = pd.read_excel(self.data_path, engine="openpyxl", index_col="ID")
        
        labels_list: list[int] = df["label"].tolist()
        texts_list = df["Texto Mascarado"].astype(str).tolist()
        
        self.dataset_size = len(texts_list)
        
        # Cria o dataset com o tokenizer correto (model_name)
        dataset = PIIDataset(texts_list, labels_list, model_name=self.model_name)
        self.data_loader = DataLoader(dataset, batch_size=self.batch_size, shuffle=True)


    def prepare_model(self):
        """Inicializa o modelo, move para o device correto e configura o otimizador."""

        self.model = PIIClassifier(model_name=self.model_name)
        self.model = self.model.to(self.device)
        
        # Otimizador dos pesos AdamW
        self.optimizer = torch.optim.AdamW(self.model.parameters(), lr=self.learning_rate)

    def train(self):
        """Executa o loop de treinamento."""
        if self.model is None or self.data_loader is None or self.optimizer is None:
            raise RuntimeError("Modelo, dados ou otimizador não inicializados. Execute load_data() e prepare_model() primeiro.")


        
        for epoch in range(self.epochs):
            acc, loss, f1, recall = train_epoch(
                model=self.model,
                data_loader=self.data_loader,
                loss_fn=self.loss_fn,
                optimizer=self.optimizer,
                device=self.device,
                n_examples=self.dataset_size
            )
            print(f"Época {epoch + 1}/{self.epochs} | Acurácia: {acc:.4f} | F1 Score: {f1:.4f} | Recall: {recall:.4f} | Loss: {loss:.4f}")

        

        self.save_model()

    def save_model(self):
        """Salva o estado do modelo no disco."""
        if not os.path.exists(self.model_save_path):
            os.makedirs(self.model_save_path)
            

        if self.model is None:
            raise RuntimeError("Modelo não inicializado. Não há nada para salvar.")
        self.model.save(self.model_save_path)

if __name__ == "__main__":
    # Exemplo de configurações fáceis de ajustar
    trainer = ModelTrainer(
        data_path="data/processed/Hackathon Participa DF Data Processado.xlsx",
        batch_size=16,      # Ajuste o tamanho do batch aqui
        learning_rate=2e-5, # Ajuste a learning rate aqui
        epochs=3,           # Ajuste o número de épocas aqui
        # device="cpu"      # Descomente para forçar CPU se necessário
    )
    
    trainer.load_data()
    trainer.prepare_model()
    trainer.train()
