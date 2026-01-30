
import pandas as pd
import pytest
import os
import sys

# Garante que a pasta src esteja no caminho de busca para os imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

SAMPLE_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/raw/AMOSTRA_e-SIC.xlsx'))
PROCESSED_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/processed/Hackathon Participa DF Data Processado.xlsx'))

def test_compare_sample_vs_processed_labels():
    """
    Compara o 'Label' do arquivo de amostra (Gabarito/Ground Truth)
    com a 'label' do arquivo processado (Predição).
    """
    
    # 1. Verifica se os arquivos existem
    assert os.path.exists(SAMPLE_FILE), f"Arquivo de amostra não encontrado em {SAMPLE_FILE}"
    assert os.path.exists(PROCESSED_FILE), f"Arquivo processado não encontrado em {PROCESSED_FILE}"

    # 2. Carrega os Dados
    df_sample = pd.read_excel(SAMPLE_FILE, engine="openpyxl")
    df_processed = pd.read_excel(PROCESSED_FILE, engine="openpyxl")

    # 3. Verifica se a coluna ID existe em ambos
    assert 'ID' in df_sample.columns, "Coluna ID faltando no arquivo de Amostra"
    assert 'ID' in df_processed.columns, "Coluna ID faltando no arquivo Processado"

    # 4. Colunas de features extraídas para análise de erros
    feature_cols = ["has_cpf", "has_cnpj", "has_email", "has_phone", "has_rg", "has_person_entity"]
    existing_feature_cols = [c for c in feature_cols if c in df_processed.columns]
    
    # Realiza o merge pelo ID para comparar lado a lado
    merged = pd.merge(
        df_sample[['ID', 'Label', 'Texto Mascarado']], 
        df_processed[['ID', 'label'] + existing_feature_cols], 
        on='ID', 
        how='inner',
        suffixes=('_sample', '_processed')
    )

    print(f"\n--- Relatório de Comparação ---")
    print(f"Total de amostras na comparação: {len(merged)}")

    # 5. Calcula Métricas Básicas
    merged['match'] = merged['Label'] == merged['label']
    accuracy = merged['match'].mean()
    
    print(f"Acurácia: {accuracy:.2%}")

    # Identifica onde houve divergência
    mismatches = merged[~merged['match']].copy()
    
    if not mismatches.empty:
        print(f"\nEncontrados {len(mismatches)} casos de divergência.")
        print("Detalhamento das divergências (quais sinais ativaram a Predição=1):")
        
        # Seleciona colunas para exibição no terminal
        display_cols = ['ID', 'Label', 'label'] + existing_feature_cols
        print(mismatches[display_cols].to_string(index=False))
        
        # Salva o detalhamento em Excel para análise manual detalhada
        mismatch_file = os.path.join(os.path.dirname(__file__), 'mismatches_detailed.xlsx')
        mismatches.to_excel(mismatch_file, index=False)
        print(f"\nDivergências detalhadas salvas em {mismatch_file}")
    else:
        print("\nTodos os rótulos coincidem perfeitamente!")

    # Garante que houve alguma comparação
    assert len(merged) > 0, "Nenhum ID em comum encontrado entre os arquivos para comparação."

if __name__ == "__main__":
    # Permite rodar o script diretamente com python
    test_compare_sample_vs_processed_labels()
