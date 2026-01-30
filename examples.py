"""
Exemplos Práticos de Uso do ShieldData

Este arquivo contém exemplos prontos para usar do sistema ShieldData.
Copie e adapte conforme necessário.
"""

# ============================================================================
# EXEMPLO 1: Classificação Simples
# ============================================================================

def exemplo_classificacao_simples():
    """Exemplo básico de classificação de um texto."""
    from src.hybrid_classifier import HybridClassifier
    
    # Inicializar classificador
    classifier = HybridClassifier(model_path="models/best_model")
    
    # Textos de exemplo
    textos = [
        "Meu CPF é 123.456.789-00 e meu telefone é (61) 99999-9999",
        "A reunião será amanhã às 14h no auditório principal",
        "Entre em contato pelo email: joao.silva@exemplo.com",
        "O projeto foi aprovado com 95% dos votos",
    ]
    
    print("=" * 70)
    print("EXEMPLO 1: Classificação Simples")
    print("=" * 70)
    
    for i, texto in enumerate(textos, 1):
        resultado = classifier.predict(texto)
        
        print(f"\n📝 Texto {i}: {texto}")
        print(f"   🔍 É PII? {'✅ SIM' if resultado['is_pii'] else '❌ NÃO'}")
        print(f"   📊 Confiança: {resultado['confidence']:.2%}")
        print(f"   💡 Razão: {resultado['reason']}")


# ============================================================================
# EXEMPLO 2: Processamento em Lote (Excel)
# ============================================================================

def exemplo_processamento_lote():
    """Processar múltiplos textos de um arquivo Excel."""
    import pandas as pd
    from src.hybrid_classifier import HybridClassifier
    
    print("\n" + "=" * 70)
    print("EXEMPLO 2: Processamento em Lote")
    print("=" * 70)
    
    # Criar dados de exemplo
    dados = {
        'ID': [1, 2, 3, 4, 5],
        'Texto': [
            "CPF: 123.456.789-00",
            "Reunião às 15h",
            "Email: contato@empresa.com",
            "Telefone: (61) 3333-4444",
            "Projeto aprovado"
        ]
    }
    
    df = pd.DataFrame(dados)
    
    # Classificar
    classifier = HybridClassifier()
    
    resultados = []
    confiancas = []
    razoes = []
    
    print("\n🔄 Processando textos...")
    for texto in df['Texto']:
        resultado = classifier.predict(texto)
        resultados.append(resultado['is_pii'])
        confiancas.append(resultado['confidence'])
        razoes.append(resultado['reason'])
    
    # Adicionar ao DataFrame
    df['É_PII'] = resultados
    df['Confiança'] = [f"{c:.2%}" for c in confiancas]
    df['Razão'] = razoes
    
    print("\n📊 Resultados:")
    print(df.to_string(index=False))
    
    # Salvar (opcional)
    # df.to_excel("data/processed/resultados_exemplo.xlsx", index=False)
    # print("\n✅ Resultados salvos em 'data/processed/resultados_exemplo.xlsx'")


# ============================================================================
# EXEMPLO 3: Ajuste de Threshold
# ============================================================================

def exemplo_ajuste_threshold():
    """Demonstrar como diferentes thresholds afetam a classificação."""
    from src.hybrid_classifier import HybridClassifier
    
    print("\n" + "=" * 70)
    print("EXEMPLO 3: Ajuste de Threshold")
    print("=" * 70)
    
    classifier = HybridClassifier()
    
    # Texto ambíguo (sem padrões óbvios)
    texto = "João da Silva mora na Rua das Flores, número 123"
    
    thresholds = [0.3, 0.5, 0.7, 0.9]
    
    print(f"\n📝 Texto: {texto}\n")
    print("Testando diferentes thresholds:")
    print("-" * 70)
    
    for threshold in thresholds:
        resultado = classifier.predict(texto, threshold=threshold)
        
        print(f"\n🎯 Threshold: {threshold}")
        print(f"   É PII? {'✅ SIM' if resultado['is_pii'] else '❌ NÃO'}")
        print(f"   Confiança: {resultado['confidence']:.2%}")
        print(f"   Razão: {resultado['reason']}")


# ============================================================================
# EXEMPLO 4: Análise Detalhada
# ============================================================================

def exemplo_analise_detalhada():
    """Mostrar detalhes completos da classificação."""
    from src.hybrid_classifier import HybridClassifier
    import json
    
    print("\n" + "=" * 70)
    print("EXEMPLO 4: Análise Detalhada")
    print("=" * 70)
    
    classifier = HybridClassifier()
    
    texto = "Meu nome é Maria Santos, CPF 987.654.321-00, email maria@exemplo.com"
    
    resultado = classifier.predict(texto)
    
    print(f"\n📝 Texto: {texto}\n")
    print("🔍 Análise Completa:")
    print("-" * 70)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    
    # Detalhes específicos
    print("\n📊 Detalhes dos Validadores:")
    print("-" * 70)
    
    if 'regex' in resultado['details']:
        print("\n✅ Regex:")
        for key, value in resultado['details']['regex'].items():
            if value:
                print(f"   • {key}: {'✓' if value else '✗'}")
    
    if 'bert' in resultado['details']:
        print(f"\n🤖 BERT:")
        print(f"   • Probabilidade: {resultado['details']['bert']:.2%}")
    
    if 'ner' in resultado['details']:
        print(f"\n🧠 NER:")
        for key, value in resultado['details']['ner'].items():
            if value > 0:
                print(f"   • {key}: {value}")


# ============================================================================
# EXEMPLO 5: Comparação de Textos
# ============================================================================

def exemplo_comparacao():
    """Comparar classificação de textos similares."""
    from src.hybrid_classifier import HybridClassifier
    
    print("\n" + "=" * 70)
    print("EXEMPLO 5: Comparação de Textos")
    print("=" * 70)
    
    classifier = HybridClassifier()
    
    pares = [
        (
            "João da Silva enviou o documento",
            "João da Silva, CPF 123.456.789-00, enviou o documento"
        ),
        (
            "Ligue para 3333-4444",
            "Ligue para (61) 99999-9999"
        ),
        (
            "Envie para contato@empresa.com",
            "Envie para o departamento de vendas"
        ),
    ]
    
    for i, (texto1, texto2) in enumerate(pares, 1):
        print(f"\n{'=' * 70}")
        print(f"Par {i}:")
        print(f"{'=' * 70}")
        
        r1 = classifier.predict(texto1)
        r2 = classifier.predict(texto2)
        
        print(f"\n📝 Texto A: {texto1}")
        print(f"   É PII? {'✅ SIM' if r1['is_pii'] else '❌ NÃO'} ({r1['confidence']:.2%})")
        
        print(f"\n📝 Texto B: {texto2}")
        print(f"   É PII? {'✅ SIM' if r2['is_pii'] else '❌ NÃO'} ({r2['confidence']:.2%})")


# ============================================================================
# EXEMPLO 6: Estatísticas de um Dataset
# ============================================================================

def exemplo_estatisticas():
    """Gerar estatísticas de um conjunto de textos."""
    from src.hybrid_classifier import HybridClassifier
    
    print("\n" + "=" * 70)
    print("EXEMPLO 6: Estatísticas de Dataset")
    print("=" * 70)
    
    classifier = HybridClassifier()
    
    # Textos de exemplo
    textos = [
        "CPF: 123.456.789-00",
        "Reunião às 15h",
        "Email: teste@exemplo.com",
        "Projeto aprovado",
        "Telefone: (61) 99999-9999",
        "João Silva participou",
        "Documento assinado",
        "CNPJ: 12.345.678/0001-90",
        "Relatório finalizado",
        "RG: 12.345.678-9",
    ]
    
    print(f"\n📊 Analisando {len(textos)} textos...\n")
    
    total_pii = 0
    confiancas = []
    razoes = {}
    
    for texto in textos:
        resultado = classifier.predict(texto)
        
        if resultado['is_pii']:
            total_pii += 1
            confiancas.append(resultado['confidence'])
            
            razao = resultado['reason']
            razoes[razao] = razoes.get(razao, 0) + 1
    
    print("📈 Estatísticas:")
    print("-" * 70)
    print(f"Total de textos: {len(textos)}")
    print(f"Contém PII: {total_pii} ({total_pii/len(textos)*100:.1f}%)")
    print(f"Não contém PII: {len(textos) - total_pii} ({(len(textos)-total_pii)/len(textos)*100:.1f}%)")
    
    if confiancas:
        print(f"\nConfiança média (PII): {sum(confiancas)/len(confiancas):.2%}")
        print(f"Confiança mínima: {min(confiancas):.2%}")
        print(f"Confiança máxima: {max(confiancas):.2%}")
    
    if razoes:
        print("\n🎯 Razões de Detecção:")
        for razao, count in sorted(razoes.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {razao}: {count} ({count/total_pii*100:.1f}%)")


# ============================================================================
# EXECUTAR TODOS OS EXEMPLOS
# ============================================================================

if __name__ == "__main__":
    print("\n" + "🛡️  " * 20)
    print("EXEMPLOS PRÁTICOS - SHIELDDATA")
    print("🛡️  " * 20)
    
    try:
        exemplo_classificacao_simples()
        exemplo_processamento_lote()
        exemplo_ajuste_threshold()
        exemplo_analise_detalhada()
        exemplo_comparacao()
        exemplo_estatisticas()
        
        print("\n" + "=" * 70)
        print("✅ Todos os exemplos executados com sucesso!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro ao executar exemplos: {e}")
        print("\n💡 Certifique-se de que:")
        print("   1. O modelo foi treinado (execute: python src/tune.py --trials 5)")
        print("   2. Você está no diretório raiz do projeto")
        print("   3. Todas as dependências estão instaladas")
