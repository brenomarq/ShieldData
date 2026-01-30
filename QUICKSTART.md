# 🚀 Guia de Início Rápido - ShieldData

Este guia irá te ajudar a começar com o ShieldData em **menos de 5 minutos**.

---

## ⚡ Instalação Rápida

```bash
# 1. Clone e entre no diretório
git clone https://github.com/seu-usuario/ShieldData.git
cd ShieldData

# 2. Instale tudo de uma vez
make install

# 3. Pronto! ✅
```

---

## 🎯 Executar o Pipeline Completo

```bash
python src/main.py
```

Isso irá:
1. ✅ Pré-processar os dados
2. ✅ Treinar o modelo BERT
3. ✅ Salvar o melhor modelo

**Tempo estimado:** 10-15 minutos (primeira execução)

---

## 💡 Usar o Classificador

### Opção 1: Python Script

Crie um arquivo `teste.py`:

```python
from src.hybrid_classifier import HybridClassifier

# Inicializar
classifier = HybridClassifier(model_path="models/best_model")

# Testar
textos = [
    "Meu CPF é 123.456.789-00",
    "O evento será amanhã às 15h",
    "Entre em contato: joao@email.com",
]

for texto in textos:
    resultado = classifier.predict(texto)
    print(f"\nTexto: {texto}")
    print(f"É PII? {resultado['is_pii']}")
    print(f"Confiança: {resultado['confidence']:.2%}")
```

Execute:
```bash
python teste.py
```

### Opção 2: Processar Arquivo Excel

```python
import pandas as pd
from src.hybrid_classifier import HybridClassifier

# Carregar seus dados
df = pd.read_excel("data/raw/meus_dados.xlsx")

# Classificar
classifier = HybridClassifier()
df['É_PII'] = df['Texto Mascarado'].apply(
    lambda x: classifier.predict(x)['is_pii']
)

# Salvar resultados
df.to_excel("data/processed/resultados.xlsx")
print("✅ Resultados salvos!")
```

---

## 📊 Ver Métricas do Modelo

```bash
python src/evaluate_hybrid.py
```

Você verá um relatório completo com:
- Precision, Recall, F1-Score
- Comparação entre modelos
- Matriz de confusão

---

## 🔧 Comandos Úteis

```bash
# Executar testes
make test

# Limpar cache
make clean

# Processar arquivo específico
python src/preprocessing.py \
  --input "data/raw/seu_arquivo.xlsx" \
  --output "data/processed/seu_arquivo_processado.xlsx"

# Treinar com hiperparâmetros customizados
python src/tune.py --trials 10
```

---

## 🆘 Problemas Comuns

### "Model not found"
```bash
# Treine o modelo primeiro
python src/tune.py --trials 5
```

### "SpaCy model not found"
```bash
python -m spacy download pt_core_news_lg
```

### "Out of memory"
Edite `src/train.py` e reduza `batch_size=8`

---

## 📚 Próximos Passos

1. ✅ Leia o [README completo](README.md)
2. ✅ Veja exemplos em `tests/`
3. ✅ Experimente com seus próprios dados
4. ✅ Ajuste os hiperparâmetros

---

## 💬 Precisa de Ajuda?

- 📖 [README Completo](README.md)
- 🐛 [Reportar Bug](https://github.com/seu-usuario/ShieldData/issues)
- 💡 [Sugestões](https://github.com/seu-usuario/ShieldData/discussions)

---

**Boa sorte! 🚀**
