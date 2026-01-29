import pandas as pd
import re
import argparse
import sys
import logging
from typing import Any
from pandas import DataFrame
from validator import Validator
from ner_detector import NamedEntityDetector

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Preprocessor:
    """
    Class responsible for preprocessing data for ShieldData.
    """
    
    @staticmethod
    def safe_clean(text: str) -> str:
        """
        Cleans text by removing excessive whitespace and handling NA values.
        """
        if pd.isna(text) or str(text).strip() == "":
            return ""

        text = str(text)
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    @staticmethod
    def generate_labels(row: "pd.Series[Any]") -> int:
        """
        Generates a binary label based on the presence of PII signals.
        Returns 1 if any PII signal is found, 0 otherwise.
        """
        cols = ["has_cpf", "has_cnpj", "has_email", "has_phone", "has_rg", "has_person_entity"]
        # Ensure we only check columns that actually exist in the row
        valid_cols = [col for col in cols if col in row.index]
        return 1 if any(row[col] == 1 for col in valid_cols) else 0

    def process_file(self, input_path: str, output_path: str):
        """
        Main processing logic: reads excel, cleans, validates, performs NER, labels, and saves.
        """
        try:
            logger.info(f"Reading file from {input_path}...")
            df: DataFrame = pd.read_excel(input_path, engine="openpyxl", index_col="ID")
        except FileNotFoundError:
            logger.error(f"File not found: {input_path}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            sys.exit(1)

        logger.info("Cleaning text...")
        if 'Texto Mascarado' not in df.columns:
             logger.error("Column 'Texto Mascarado' not found in input file.")
             sys.exit(1)

        df['Texto Mascarado'] = df['Texto Mascarado'].apply(self.safe_clean)

        logger.info("Validating Regex patterns (CPF, CNPJ, etc)...")
        # Validate patterns
        df_labels = df['Texto Mascarado'].apply(Validator.validate_all_types).apply(pd.Series)
        df_labels = df_labels.astype(int)
        df = df.join(df_labels)

        logger.info("Running Named Entity Recognition...")
        ner_detector = NamedEntityDetector()
        sinais_list = df['Texto Mascarado'].apply(ner_detector.extract_signals).tolist()
        df_sinais = pd.DataFrame(sinais_list, index=df.index)
        df = df.join(df_sinais)

        logger.info("Generating labels...")
        df['label'] = df.apply(self.generate_labels, axis=1)

        logger.info("Removing duplicates...")
        mask = df.duplicated(subset=["Texto Mascarado"], keep="first")
        removidos = df[mask]
        df = df[~mask]
        
        if not removidos.empty:
            logger.info(f"Removed {len(removidos)} duplicate rows.")

        logger.info(f"Saving processed data to {output_path}...")
        try:
            df.to_excel(output_path)
            logger.info("Processing complete.")
        except Exception as e:
             logger.error(f"Error saving file: {e}")
             sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="ShieldData Preprocessing Script")
    parser.add_argument("--input", type=str, required=True, help="Path to input Excel file.")
    parser.add_argument("--output", type=str, required=True, help="Path to output Excel file.")
    
    args = parser.parse_args()
    
    preprocessor = Preprocessor()
    preprocessor.process_file(args.input, args.output)

if __name__ == "__main__":
    main()
