from sklearn.metrics import f1_score, accuracy_score
import torch
import numpy as np

class ScoreCalculator:
    """
    Utility class to calculate model performance metrics.
    """
    
    @staticmethod
    def calculate_f1(y_true: list | np.ndarray | torch.Tensor, y_pred: list | np.ndarray | torch.Tensor, average: str = 'weighted') -> float:
        """
        Calcoulate F1 Score.
        
        Args:
            y_true: True labels.
            y_pred: Predicted labels.
            average: 'binary' for binary classification (default), 
                     'micro', 'macro', 'weighted' fo multiclass.
        
        Returns:
            float: F1 Score.
        """
        # Ensure inputs are numpy arrays/lists on CPU
        y_true = ScoreCalculator._to_numpy(y_true)
        y_pred = ScoreCalculator._to_numpy(y_pred)
        
        return float(f1_score(y_true, y_pred, average=average))
    
    @staticmethod
    def calculate_metrics(y_true: list | np.ndarray | torch.Tensor, y_pred: list | np.ndarray | torch.Tensor) -> dict[str, float]:
        """
        Calculate common metrics: Accuracy and F1 Score (weighted).
        """
        y_true = ScoreCalculator._to_numpy(y_true)
        y_pred = ScoreCalculator._to_numpy(y_pred)
        
        return {
            "accuracy": float(accuracy_score(y_true, y_pred)),
            "f1_score": float(f1_score(y_true, y_pred, average='weighted'))
        }

    @staticmethod
    def _to_numpy(data):
        if isinstance(data, torch.Tensor):
            return data.detach().cpu().numpy()
        
        # Handle list of tensors (e.g., from MPS/GPU) by stacking and moving to CPU
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], torch.Tensor):
            return torch.stack(data).detach().cpu().numpy()
            
        return np.array(data)
