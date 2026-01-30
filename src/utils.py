"""
Módulo de utilitários compartilhados para o projeto ShieldData.

Este módulo contém funções auxiliares que são usadas em múltiplos
componentes do projeto, evitando duplicação de código.
"""

import os
import torch
from typing import Optional


def get_best_device() -> torch.device:
    """
    Detecta o melhor dispositivo disponível para computação com PyTorch.
    
    Ordem de prioridade:
    1. CUDA (GPU NVIDIA)
    2. MPS (GPU Apple Silicon)
    3. CPU (fallback)
    
    Returns:
        torch.device: O melhor dispositivo disponível
    """
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return torch.device("mps")
    else:
        return torch.device("cpu")


def validate_file_exists(file_path: str, error_message: Optional[str] = None) -> bool:
    """
    Valida se um arquivo existe.
    
    Args:
        file_path: Caminho do arquivo a ser validado
        error_message: Mensagem de erro customizada (opcional)
    
    Returns:
        bool: True se o arquivo existe, False caso contrário
    
    Raises:
        FileNotFoundError: Se o arquivo não existir e error_message for fornecido
    """
    exists = os.path.exists(file_path)
    
    if not exists and error_message:
        raise FileNotFoundError(error_message)
    
    return exists


def ensure_dir_exists(dir_path: str) -> None:
    """
    Garante que um diretório existe, criando-o se necessário.
    
    Args:
        dir_path: Caminho do diretório
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
