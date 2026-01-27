from sklearn.metrics import f1_score, accuracy_score, recall_score
import torch
import numpy as np

class ScoreCalculator:
    """
    Classe utilitária para calcular métricas de desempenho do modelo.
    """
    
    @staticmethod
    def calculate_f1(y_true: list | np.ndarray | torch.Tensor, y_pred: list | np.ndarray | torch.Tensor, average: str = 'weighted') -> float:
        """
        Calcula o F1 Score.
        
        Args:
            y_true: Rótulos verdadeiros.
            y_pred: Rótulos previstos.
            average: 'binary' para classificação binária (padrão), 
                     'micro', 'macro', 'weighted' para multiclasse.
        
        Returns:
            float: F1 Score.
        """
        # Garante que as entradas sejam arrays/listas numpy na CPU
        y_true = ScoreCalculator._to_numpy(y_true)
        y_pred = ScoreCalculator._to_numpy(y_pred)
        
        return float(f1_score(y_true, y_pred, average=average))
    
    @staticmethod
    def calculate_recall(y_true: list | np.ndarray | torch.Tensor, y_pred: list | np.ndarray | torch.Tensor, average: str = 'weighted') -> float:
        """
        Calcula o Recall.
        
        Args:
            y_true: Rótulos verdadeiros.
            y_pred: Rótulos previstos.
            average: 'binary' para classificação binária (padrão), 
                     'micro', 'macro', 'weighted' para multiclasse.
        
        Returns:
            float: Recall.
        """
        # Garante que as entradas sejam arrays/listas numpy na CPU
        y_true = ScoreCalculator._to_numpy(y_true)
        y_pred = ScoreCalculator._to_numpy(y_pred)
        
        return float(recall_score(y_true, y_pred, average=average))

    @staticmethod
    def calculate_metrics(y_true: list | np.ndarray | torch.Tensor, y_pred: list | np.ndarray | torch.Tensor) -> dict[str, float]:
        """
        Calcula métricas comuns: Acurácia, F1 Score (ponderado) e Recall (ponderado).
        """
        y_true = ScoreCalculator._to_numpy(y_true)
        y_pred = ScoreCalculator._to_numpy(y_pred)
        
        return {
            "accuracy": float(accuracy_score(y_true, y_pred)),
            "f1_score": float(f1_score(y_true, y_pred, average='weighted')),
            "recall": float(recall_score(y_true, y_pred, average='weighted'))
        }

    @staticmethod
    def _to_numpy(data):
        if isinstance(data, torch.Tensor):
            return data.detach().cpu().numpy()
        
        # Lida com lista de tensores (ex: de MPS/GPU) empilhando e movendo para a CPU
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], torch.Tensor):
            return torch.stack(data).detach().cpu().numpy()
            
        return np.array(data)
