import sys
import os
import numpy as np
import torch
from sklearn.metrics import recall_score as sk_recall_score

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from score_calculator import ScoreCalculator

def test_score_calculator():
    print("Testing ScoreCalculator recall calculation...")

    # Create dummy data
    y_true = np.array([0, 1, 1, 0, 1, 0])
    y_pred = np.array([0, 1, 0, 0, 1, 1])

    # Calculate expected recall using sklearn directly
    expected_recall = sk_recall_score(y_true, y_pred, average='weighted')
    
    # Calculate using ScoreCalculator
    calculated_recall = ScoreCalculator.calculate_recall(y_true, y_pred)
    
    print(f"Expected Recall: {expected_recall}")
    print(f"Calculated Recall: {calculated_recall}")
    
    # Assert almost equal
    assert np.isclose(expected_recall, calculated_recall), "Recall calculation mismatch!"
    
    # Test calculate_metrics
    metrics = ScoreCalculator.calculate_metrics(y_true, y_pred)
    print("Metrics calculated:", metrics)
    
    assert 'recall' in metrics, "Recall key missing in metrics!"
    assert np.isclose(metrics['recall'], expected_recall), "Recall in metrics mismatch!"
    
    print("\nTest passed successfully!")

def test_torch_tensors():
    print("\nTesting ScoreCalculator with Torch Tensors...")
    
    y_true = torch.tensor([0, 1, 1, 0, 1, 0])
    y_pred = torch.tensor([0, 1, 0, 0, 1, 1])
    
    expected_recall = sk_recall_score(y_true.numpy(), y_pred.numpy(), average='weighted')
    calculated_recall = ScoreCalculator.calculate_recall(y_true, y_pred)
    
    print(f"Expected Recall: {expected_recall}")
    print(f"Calculated Recall: {calculated_recall}")
    
    assert np.isclose(expected_recall, calculated_recall), "Recall calculation mismatch with Tensors!"
    print("Tensor test passed successfully!")

if __name__ == "__main__":
    test_score_calculator()
    test_torch_tensors()
