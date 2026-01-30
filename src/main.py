import os
import sys
import logging
import argparse

# Ensure src is in path so we can import modules
sys.path.append(os.path.join(os.getcwd(), 'src'))

from preprocessing import Preprocessor
from tune import main as tune_main

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_pipeline():
    """
    Executes the full ShieldData pipeline:
    1. Preprocessing (Clean + NER + Regex Validation)
    2. Hyperparameter Tuning (Optuna) -> Trains and saves best model
    """
    
    # --- Configuration ---
    raw_data_path = "data/raw/AMOSTRA_e-SIC.xlsx"
    processed_data_path = "data/processed/AMOSTRA_e-SIC_processed.xlsx"
    # ---------------------

    logger.info("="*60)
    logger.info("🚀 STARTING SHIELDDATA PIPELINE")
    logger.info("="*60)

    # 1. Preprocessing
    logger.info(f"Step 1: Running Preprocessing on {raw_data_path}...")
    
    if not os.path.exists(raw_data_path):
        logger.error(f"❌ Raw data file not found: {raw_data_path}")
        sys.exit(1)

    try:
        preprocessor = Preprocessor()
        # Important: clean_only=False ensures we run NER and Regex validation
        preprocessor.process_file(input_path=raw_data_path, output_path=processed_data_path, clean_only=False)
        logger.info(f"✅ Preprocessing completed. Saved to {processed_data_path}")
    except Exception as e:
        logger.error(f"❌ Preprocessing failed: {e}")
        sys.exit(1)

    # 2. Hyperparameter Tuning & Training
    logger.info("="*60)
    logger.info("Step 2: Starting Hyperparameter Tuning (Optuna) & Final Training...")
    logger.info("NOTE: This step will automatically train and save the BEST model found.")
    logger.info("="*60)

    try:
        # We call the main function from tune.py. 
        # Note: tune.py parses args, so we might need to manipulate sys.argv or refactor tune.py slightly if we want to pass args programmatically.
        # For now, let's assume default behavior or simple flag injection if needed.
        
        # Simulating command line arguments for the tune script if necessary
        # Currently tune.py uses argparse for --trials. Let's default to a reasonable number if not specified, 
        # or we could make this configurable via main.py arguments.
        
        # Let's force a default of 10 trials for the full pipeline run, or respect sys.argv if provided.
        # Ideally, we should refactor tune.py to accept arguments in a function, but to keep changes minimal as requested:
        if len(sys.argv) == 1:
             sys.argv.append("--trials")
             sys.argv.append("5") # Default to 5 trials for a quick but effective run

        tune_main()
        
        logger.info("="*60)
        logger.info("✅ PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("The best BERT model has been saved to 'models/best_model'")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"❌ Tuning/Training failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()
