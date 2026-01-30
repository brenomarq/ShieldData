import os
import sys
import logging
import argparse

# Garante que o diretório src está no path para importação de módulos
sys.path.append(os.path.join(os.getcwd(), 'src'))

from preprocessing import Preprocessor
from tune import main as tune_main

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_pipeline():
    """
    Executes the full ShieldData pipeline:
    1. Preprocessing (Clean + NER + Regex Validation)
    2. Hyperparameter Tuning (Optuna) -> Trains and saves best model
    """
    
    # --- Configuração ---
    raw_data_path = "data/raw/AMOSTRA_e-SIC.xlsx"
    processed_data_path = "data/processed/AMOSTRA_e-SIC_processed.xlsx"
    # --------------------

    logger.info("="*60)
    logger.info("🚀 STARTING SHIELDDATA PIPELINE")
    logger.info("="*60)

    # 1. Pré-processamento
    logger.info(f"Etapa 1: Executando pré-processamento em {raw_data_path}...")
    
    if not os.path.exists(raw_data_path):
        logger.error(f"❌ Arquivo de dados brutos não encontrado: {raw_data_path}")
        sys.exit(1)

    try:
        preprocessor = Preprocessor()
        # Importante: clean_only=False garante que executamos NER e validação Regex
        preprocessor.process_file(input_path=raw_data_path, output_path=processed_data_path, clean_only=False)
        logger.info(f"✅ Pré-processamento concluído. Salvo em {processed_data_path}")
    except Exception as e:
        logger.error(f"❌ Pré-processamento falhou: {e}")
        sys.exit(1)

    # 2. Ajuste de Hiperparâmetros e Treinamento
    logger.info("="*60)
    logger.info("Etapa 2: Iniciando ajuste de hiperparâmetros (Optuna) e treinamento final...")
    logger.info("NOTA: Esta etapa irá automaticamente treinar e salvar o MELHOR modelo encontrado.")
    logger.info("="*60)

    try:
        # Chamamos a função main do tune.py
        # Nota: tune.py faz parse de argumentos, então precisamos manipular sys.argv
        # ou refatorar tune.py para aceitar argumentos programaticamente.
        
        # Define número padrão de trials se não especificado
        # Idealmente, deveríamos refatorar tune.py para aceitar argumentos em uma função,
        # mas para manter mudanças mínimas:
        if len(sys.argv) == 1:
             sys.argv.extend(["--trials", "5"])  # Padrão de 5 trials para execução rápida mas efetiva

        tune_main()
        
        logger.info("="*60)
        logger.info("✅ PIPELINE CONCLUÍDO COM SUCESSO")
        logger.info("O melhor modelo BERT foi salvo em 'models/best_model'")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"❌ Ajuste/Treinamento falhou: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()
