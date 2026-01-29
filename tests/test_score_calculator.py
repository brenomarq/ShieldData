import sys
import os
import numpy as np
import torch
import pytest
from sklearn.metrics import recall_score as sk_recall_score

# Ensure src is in path for imports
sys.path.append(os.path.join(os.getcwd(), 'src'))

from score_calculator import ScoreCalculator

def test_calculate_recall_numpy():
    """Test ScoreCalculator recall calculation with numpy arrays."""
    # Create dummy data
    y_true = np.array([0, 1, 1, 0, 1, 0])
    y_pred = np.array([0, 1, 0, 0, 1, 1])

    # Calculate expected using sklearn
    expected_recall = sk_recall_score(y_true, y_pred, average='weighted')
    
    # Calculate using ScoreCalculator
    calculated_recall = ScoreCalculator.calculate_recall(y_true, y_pred)
    
    # Assert
    assert np.isclose(expected_recall, calculated_recall), "Recall calculation mismatch (numpy)!"

def test_calculate_recall_torch():
    """Test ScoreCalculator recall calculation with torch tensors."""
    y_true = torch.tensor([0, 1, 1, 0, 1, 0])
    y_pred = torch.tensor([0, 1, 0, 0, 1, 1])
    
    expected_recall = sk_recall_score(y_true.numpy(), y_pred.numpy(), average='weighted')
    calculated_recall = ScoreCalculator.calculate_recall(y_true, y_pred)
    
    assert np.isclose(expected_recall, calculated_recall), "Recall calculation mismatch (torch)!"

def test_calculate_metrics():
    """Test ScoreCalculator.calculate_metrics returns all expected keys and values."""
    y_true = np.array([0, 1, 1, 0, 1, 0])
    y_pred = np.array([0, 1, 0, 0, 1, 1])
    
    encoded_recall = sk_recall_score(y_true, y_pred, average='weighted')
    
    metrics = ScoreCalculator.calculate_metrics(y_true, y_pred)
    
    assert 'recall' in metrics, "metrics dict missing 'recall'"
    assert 'f1_score' in metrics, "metrics dict missing 'f1_score'"
    assert 'accuracy' in metrics, "metrics dict missing 'accuracy'"
    
    assert np.isclose(metrics['recall'], encoded_recall), "Recall value in metrics mismatch!"
