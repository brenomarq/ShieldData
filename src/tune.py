import argparse
import optuna
import logging
import sys
import os

# Garante que src está no path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from train import ModelTrainer

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def objective(trial):
    """
    Função de objetivo para o Optuna.
    O Optuna vai chamar essa função várias vezes com parâmetros diferentes
    que ele "sugere" baseado nos testes anteriores.
    """
    
    # 1. Definir o espaço de busca (Hyperparameter Search Space)
    learning_rate = trial.suggest_float("learning_rate", 1e-6, 1e-4, log=True)
    batch_size = trial.suggest_categorical("batch_size", [8, 16, 32])
    epochs = trial.suggest_int("epochs", 2, 5)
    
    # Caminho dos dados
    data_path = "data/processed/AMOSTRA_e-SIC_processed.xlsx"
    
    # Verifica se os dados existem antes de tentar treinar
    if not os.path.exists(data_path):
        logger.error(f"Arquivo de dados não encontrado: {data_path}")
        logger.error("Por favor, execute 'make process' primeiro.")
        raise FileNotFoundError(f"{data_path} not found")

    logger.info(f"Iniciando Trial {trial.number} com: lr={learning_rate}, batch={batch_size}, epochs={epochs}")

    # 2. Instanciar e rodar o treino
    # Usamos um diretório temporário ou sufixo para não sobrescrever o modelo principal toda hora
    model_save_path = f"models/trial_{trial.number}"
    
    trainer = ModelTrainer(
        data_path=data_path,
        model_save_path=model_save_path,
        batch_size=batch_size,
        learning_rate=learning_rate,
        epochs=epochs,
        device=None  # Deixe None para detectar automaticamente (usará MPS no Mac)
    )
    
    trainer.load_data()
    trainer.prepare_model()
    
    # O train() agora retorna as métricas finais
    metrics = trainer.train()
    
    # 3. Retornar a métrica que queremos otimizar (MAXIMIZAR o F1 Score)
    f1_score = metrics['f1']
    
    return f1_score

def main():
    parser = argparse.ArgumentParser(description="Script de Otimização de Hiperparâmetros com Optuna")
    parser.add_argument("--trials", type=int, default=10, help="Número de tentativas (trials) que o Optuna fará.")
    args = parser.parse_args()

    logger.info(f"Iniciando estudo com {args.trials} tentativas...")
    
    # Cria o estudo do Optuna
    study = optuna.create_study(direction="maximize")  # Queremos MAXIMIZAR o F1
    study.optimize(objective, n_trials=args.trials)

    print("\n" + "="*40)
    print("RESULTADOS DA OTIMIZAÇÃO")
    print("="*40)
    print(f"Melhor trial (Tentativa #{study.best_trial.number}):")
    print(f"  Valor (F1 Score): {study.best_value:.4f}")
    print("  Melhores Parâmetros:")
    for key, value in study.best_params.items():
        print(f"    {key}: {value}")
    print("="*40)

    # 4. Treinar o modelo final com os melhores parâmetros e salvar
    print("\nTreinando o modelo final com os melhores parâmetros...")
    best_params = study.best_params
    final_model_path = "models/best_model"
    
    final_trainer = ModelTrainer(
        data_path="data/processed/AMOSTRA_e-SIC_processed.xlsx",
        model_save_path=final_model_path,
        batch_size=best_params["batch_size"],
        learning_rate=best_params["learning_rate"],
        epochs=best_params["epochs"]
    )
    
    final_trainer.load_data()
    final_trainer.prepare_model()
    final_trainer.train()
    
    print(f"\nModelo final otimizado salvo em: {final_model_path}")
    print("="*40)

if __name__ == "__main__":
    main()
