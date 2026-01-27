import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModel
from typing import List, Any, cast
from score_calculator import ScoreCalculator

# ==============================================================================
# 1. O PREPARADOR DE DADOS (Dataset)
# ==============================================================================
class PIIDataset(Dataset[Any]):
    """
    Responsável por pegar seus textos crus e labels, tokenizá-los e entregar
    tensores prontos para o PyTorch.
    
    O BERT não lê strings, ele lê 'input_ids' (índices numéricos de vocabulário)
    e 'attention_mask' (para ignorar preenchimentos/padding).
    """
    def __init__(self, texts: List[str], labels: List[int], model_name: str = "neuralmind/bert-base-portuguese-cased", max_len: int = 128):
        self.texts: List[str] = texts
        self.labels = labels
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.max_len = max_len

    def __len__(self):
        # O DataLoader precisa saber quantos exemplos existem no total
        return len(self.texts)

    def __getitem__(self, item: int) -> dict[str, torch.Tensor]:
        # Esse método é chamado para pegar 1 exemplo específico pelo índice
        text = str(self.texts[item])
        label = self.labels[item]

        # Tokenização: Transforma "Eu gosto de Python" em [101, 234, 567, ..., 102]
        encoding = self.tokenizer(
            text,
            add_special_tokens=True,    # Adiciona [CLS] no início e [SEP] no fim
            max_length=self.max_len,
            return_token_type_ids=False,
            padding='max_length',       # Preenche frases curtas com 0s até max_len
            truncation=True,            # Corta frases longas
            return_attention_mask=True, # Cria a máscara (1 para texto real, 0 para padding)
            return_tensors='pt',        # Retorna tensores do PyTorch
        )

        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }


# ==============================================================================
# 2. O MODELO (BERT + Classificador)
# ==============================================================================
class PIIClassifier(nn.Module):
    """
    Aqui montamos o corpo e a cabeça do modelo.
    - Corpo: BERT pré-treinado (extrai características complexas do texto).
    - Cabeça: Camada Linear simples (toma a decisão final entre 0 e 1).
    """
    def __init__(self, model_name: str = "neuralmind/bert-base-portuguese-cased", n_classes: int = 2):
        super(PIIClassifier, self).__init__()
        # Carregamos o cérebro pré-treinado
        self.bert = AutoModel.from_pretrained(model_name)
        
        # Adicionamos uma camada de Dropout (desliga neurônios aleatórios para evitar decorar dados/overfitting)
        self.drop = nn.Dropout(p=0.3)
        
        # A camada final: transforma 768 características do BERT em n_classes (2: Sim/Não)
        hidden_size = cast(int, self.bert.config.hidden_size) # type: ignore
        self.out = nn.Linear(hidden_size, n_classes)

    def forward(self, input_ids: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
        # 1. Passar os dados pelo BERT
        # pooled_output é basicamente o vetor resumo da frase inteira (token [CLS])
        outputs = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        pooled_output = outputs.pooler_output 

        # 2. Passar pelo Dropout
        output = self.drop(pooled_output)

        # 3. Passar pela camada de decisão final
        return self.out(output)

    def save(self, path: str):
        """Salva os pesos do modelo e o tokenizer."""
        torch.save(self.state_dict(), f"{path}/model_state.bin")
        # É importante salvar a config se quisermos carregar dinamicamente depois,
        # mas por hora, assumimos que quem carrega sabe os hiperparâmetros.

    @classmethod
    def load(cls, path: str, model_name: str = "neuralmind/bert-base-portuguese-cased", n_classes: int = 2):
        """Carrega um modelo treinado do disco."""
        model = cls(model_name, n_classes)
        model.load_state_dict(torch.load(f"{path}/model_state.bin", map_location=torch.device('cpu')))
        return model


# ==============================================================================
# 3. O LOOP DE TREINO (Exemplo de função)
# ==============================================================================
def train_epoch(model: nn.Module, data_loader: DataLoader[Any], loss_fn: nn.Module, optimizer: torch.optim.Optimizer, device: torch.device, n_examples: int) -> tuple[float, float, float]:
    model = model.train() # Coloca o modelo em modo de treino (ativa dropout, etc)
    
    losses: List[float] = []
    correct_predictions: int | torch.Tensor = 0
    
    all_preds = []
    all_targets = []
    
    for d in data_loader:
        input_ids = d["input_ids"].to(device)
        attention_mask = d["attention_mask"].to(device)
        targets = d["labels"].to(device)

        # A. Foward Pass: O modelo faz a previsão
        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        # B. Cálculo do Erro: Quão longe a previsão estava do real?
        _, preds = torch.max(outputs, dim=1)
        loss = loss_fn(outputs, targets)

        correct_predictions += torch.sum(preds == targets)
        losses.append(loss.item())

        all_preds.extend(preds)
        all_targets.extend(targets)

        # C. Backward Pass: "Aprender" com o erro
        loss.backward()  # Calcula gradientes (direção do ajuste)
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0) # Evita explosão de gradientes
        optimizer.step() # Atualiza os pesos
        optimizer.zero_grad() # Zera gradientes para o próximo passo

    accuracy = correct_predictions.float() / n_examples # type: ignore
    
    # Calculate F1 using ScoreCalculator
    # Note: all_preds and all_targets are lists of tensors, we can stack them or pass as list
    # ScoreCalculator handles list of tensors if we ensure they are clean
    f1 = ScoreCalculator.calculate_f1(all_targets, all_preds)
    
    return accuracy.item(), sum(losses) / len(losses), f1