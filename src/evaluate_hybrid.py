import pandas as pd
import logging
from hybrid_classifier import HybridClassifier
from piiclassifier import PIIClassifier
from score_calculator import ScoreCalculator
import torch
from sklearn.metrics import classification_report

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def evaluate():
    data_path = "data/processed/AMOSTRA_e-SIC_processed.xlsx"
    model_path = "models/best_model"
    
    logger.info(f"Carregando dados de {data_path}...")
    df = pd.read_excel(data_path, index_col=0) # Assuming ID is index
    
    # Check correct column for text
    text_col = "Texto Mascarado"
    if text_col not in df.columns:
         logger.error(f"Coluna {text_col} não encontrada.")
         return

    texts = df[text_col].astype(str).tolist()
    # Rótulos reais (Ground Truth)
    # Nota: Usando 'Label' como padrão recente, mas fallback para 'label' se não encontrado
    label_col = "Label" if "Label" in df.columns else "label"
    true_labels = df[label_col].tolist()

    logger.info("Inicializando classificadores...")
    # 1. Classificador Híbrido
    hybrid = HybridClassifier(model_path=model_path)
    
    # 2. BERT Standalone (para comparação) - reutilizamos o modelo interno do hybrid para economizar memória/tempo
    bert_only = hybrid.bert_model

    logger.info(f"Avaliando {len(texts)} exemplos...")
    
    hybrid_preds = []
    bert_preds = []
    baseline_preds = []
    
    # Loop de avaliação
    for i, text in enumerate(texts):
        if i % 20 == 0:
            print(f"Processando {i}/{len(texts)}...", end="\r")
        
        # A. Previsão Híbrida
        h_result = hybrid.predict(text)
        hybrid_preds.append(1 if h_result["is_pii"] else 0)
        
        # B. Previsão BERT Puro
        # Reutilizando a lógica de HybridClassifier._get_bert_probability manualmente
        try:
             prob = hybrid._get_bert_probability(text)
             bert_preds.append(1 if prob >= 0.5 else 0)
        
        except Exception:
             bert_preds.append(0)
        
        # C. Previsão Baseline (Apenas Regex + NER, sem BERT)
        # Lógica: Se qualquer Regex bater OU qualquer entidade NER for encontrada -> É PII
        # Essa é a lógica tradicional determinística.
        is_baseline_pii = (
            h_result["details"]["regex"]["has_cpf"] or
            h_result["details"]["regex"]["has_cnpj"] or
            h_result["details"]["regex"]["has_email"] or
            h_result["details"]["regex"]["has_phone"] or
            h_result["details"]["regex"]["has_rg"] or
            h_result["details"]["ner"]["has_person_entity"]
        )
        baseline_preds.append(1 if is_baseline_pii else 0)

    print("\n" + "="*60)
    print("RELATÓRIO DE COMPARAÇÃO")
    print("="*60)
    
    # Métricas BERT Puro
    print("\n--- MODELO BERT PURO (Overfitted) ---")
    print(classification_report(true_labels, bert_preds, target_names=["Não PII", "PII"]))
    
    # Métricas Baseline (Só Regras)
    print("\n--- BASELINE (Apenas Regex + SpaCy) ---")
    print(classification_report(true_labels, baseline_preds, target_names=["Não PII", "PII"]))

    # Métricas Híbrido
    print("\n--- CLASSIFICADOR HÍBRIDO (Ensemble) ---")
    print(classification_report(true_labels, hybrid_preds, target_names=["Não PII", "PII"]))

    # Cálculo manual simples para confirmação
    bert_f1 = ScoreCalculator.calculate_f1(true_labels, bert_preds)
    baseline_f1 = ScoreCalculator.calculate_f1(true_labels, baseline_preds)
    hybrid_f1 = ScoreCalculator.calculate_f1(true_labels, hybrid_preds)
    
    print("="*60)
    print(f"BERT F1-Score:     {bert_f1:.4f}")
    print(f"Baseline F1-Score: {baseline_f1:.4f}")
    print(f"Híbrido F1-Score:  {hybrid_f1:.4f}")
    print("="*60)
    
    if hybrid_f1 > baseline_f1:
        print("✅ O Híbrido superou o Baseline (Regex/SpaCy sozinhos)!")
    elif hybrid_f1 < baseline_f1:
        print("⚠️ O Híbrido não superou a Baseline.")
    else:
        print("😐 Empate entre Híbrido e Baseline.")

if __name__ == "__main__":
    evaluate()
