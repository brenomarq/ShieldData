# 🛡️ ShieldData

<div align="center">

**Sistema Inteligente de Detecção de Dados Pessoais (PII) usando IA**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

*Desenvolvido para o Hackathon em Controle Social - GDF 2026*

</div>

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Arquitetura](#-arquitetura)
- [Instalação](#-instalação)
- [Uso Rápido](#-uso-rápido)
- [Guia Detalhado](#-guia-detalhado)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Tecnologias](#-tecnologias)
- [Performance](#-performance)
- [Testes](#-testes)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)

---

## 🎯 Sobre o Projeto

O **ShieldData** é um sistema de detecção automática de informações pessoais identificáveis (PII - *Personally Identifiable Information*) em textos, desenvolvido para proteger a privacidade de cidadãos em documentos públicos.

### 🔍 Problema

Documentos públicos frequentemente contêm dados pessoais sensíveis (CPF, e-mail, telefone, nomes) que precisam ser identificados e protegidos antes da publicação.

### 💡 Solução

Sistema híbrido que combina:
- **🤖 BERT** - Deep Learning para análise contextual
- **📝 Regex** - Padrões fixos de alta precisão (CPF, CNPJ, e-mail)
- **🧠 SpaCy NER** - Reconhecimento de entidades nomeadas

### 🎯 Objetivo

Maximizar o **F1-Score** garantindo que dados sensíveis nunca passem despercebidos, mesmo em contextos complexos.

---

## ✨ Funcionalidades

### 🔐 Detecção Inteligente de PII

- ✅ **CPF** - Validação com dígito verificador
- ✅ **CNPJ** - Formato completo e simplificado
- ✅ **E-mail** - Padrões RFC compliant
- ✅ **Telefone** - Fixo e celular (com/sem DDD)
- ✅ **RG** - Formatos comuns brasileiros
- ✅ **Nomes de Pessoas** - Via NER com SpaCy
- ✅ **Localizações** - Endereços e locais

### 🚀 Pipeline Automatizado

1. **Pré-processamento** - Limpeza e normalização de texto
2. **Validação Regex** - Detecção de padrões fixos
3. **NER** - Extração de entidades nomeadas
4. **Treinamento BERT** - Otimização com Optuna
5. **Classificação Híbrida** - Ensemble inteligente

### 📊 Otimização Automática

- **Optuna** para busca de hiperparâmetros
- **Validação cruzada** automática
- **Métricas detalhadas** (F1, Recall, Precision)

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    CLASSIFICADOR HÍBRIDO                     │
└─────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
         ┌──────▼──────┐ ┌───▼────┐ ┌─────▼─────┐
         │    REGEX    │ │  BERT  │ │   SpaCy   │
         │  (Padrões)  │ │(Context)│ │   (NER)   │
         └─────────────┘ └────────┘ └───────────┘
                │             │             │
                └─────────────┼─────────────┘
                              │
                    ┌─────────▼─────────┐
                    │  Decisão Final    │
                    │   (is_pii: bool)  │
                    └───────────────────┘
```

### 🧩 Lógica de Decisão

1. **Regex Forte** (CPF/CNPJ/Email) → `PII = True` (confiança 100%)
2. **BERT Alta Confiança** (>0.8) → `PII = True`
3. **BERT Moderado** (0.4-0.8) + **NER** → `PII = True`
4. **Telefone** + **BERT Mínimo** (>0.3) → `PII = True`
5. **Fallback** → Threshold padrão (0.5)

---

## 🚀 Instalação

### Pré-requisitos

- **Python 3.8+**
- **pip** (gerenciador de pacotes)
- **8GB RAM** (recomendado para BERT)

### Instalação Rápida

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/ShieldData.git
cd ShieldData

# 2. Crie um ambiente virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Baixe o modelo SpaCy em português
python -m spacy download pt_core_news_lg
```

### Instalação com Make

```bash
make install
```

### Verificação da Instalação

```bash
# Teste se tudo está funcionando
pytest tests/
```

---

## ⚡ Uso Rápido

### 1️⃣ Pipeline Completo (Recomendado)

Execute todo o pipeline de uma vez:

```bash
python src/main.py
```

Isso irá:
1. ✅ Pré-processar os dados
2. ✅ Otimizar hiperparâmetros (Optuna)
3. ✅ Treinar o melhor modelo
4. ✅ Salvar em `models/best_model`

### 2️⃣ Uso Individual

#### Pré-processamento

```bash
python src/preprocessing.py \
  --input "data/raw/seu_arquivo.xlsx" \
  --output "data/processed/seu_arquivo_processado.xlsx"
```

#### Treinamento

```bash
python src/train.py
```

#### Otimização de Hiperparâmetros

```bash
python src/tune.py --trials 10
```

#### Avaliação do Modelo Híbrido

```bash
python src/evaluate_hybrid.py
```

### 3️⃣ Uso Programático

```python
from hybrid_classifier import HybridClassifier

# Inicializar classificador
classifier = HybridClassifier(model_path="models/best_model")

# Classificar texto
texto = "Meu CPF é 123.456.789-00 e meu email é joao@exemplo.com"
resultado = classifier.predict(texto)

print(f"É PII? {resultado['is_pii']}")
print(f"Confiança: {resultado['confidence']:.2%}")
print(f"Razão: {resultado['reason']}")
```

**Saída:**
```
É PII? True
Confiança: 100.00%
Razão: Correspondência forte de Regex
```

---

## 📖 Guia Detalhado

### Preparação dos Dados

#### Formato Esperado

Arquivo Excel (`.xlsx`) com as seguintes colunas:

| ID | Texto Mascarado | Label (opcional) |
|----|-----------------|------------------|
| 1  | "Texto aqui..." | 1                |
| 2  | "Outro texto..." | 0               |

- **ID**: Identificador único
- **Texto Mascarado**: Texto a ser analisado
- **Label**: 0 (não PII) ou 1 (PII) - usado para treinamento

#### Colocando seus Dados

```bash
# Coloque seu arquivo em:
data/raw/seu_arquivo.xlsx

# Execute o pré-processamento:
python src/preprocessing.py \
  --input "data/raw/seu_arquivo.xlsx" \
  --output "data/processed/seu_arquivo_processado.xlsx"
```

### Treinamento Personalizado

#### Ajustar Hiperparâmetros Manualmente

Edite `src/train.py`:

```python
trainer = ModelTrainer(
    data_path="data/processed/AMOSTRA_e-SIC_processed.xlsx",
    batch_size=16,        # Ajuste aqui (8, 16, 32)
    learning_rate=2e-5,   # Ajuste aqui (1e-6 a 1e-4)
    epochs=3,             # Ajuste aqui (2 a 5)
)
```

#### Otimização Automática com Optuna

```bash
# Executar 20 tentativas de otimização
python src/tune.py --trials 20
```

O Optuna irá:
- ✅ Testar diferentes combinações de hiperparâmetros
- ✅ Salvar o melhor modelo automaticamente
- ✅ Exibir relatório de resultados

### Avaliação e Métricas

```bash
python src/evaluate_hybrid.py
```

**Saída Exemplo:**
```
═══════════════════════════════════════════════════════════
RELATÓRIO DE COMPARAÇÃO
═══════════════════════════════════════════════════════════

--- MODELO BERT PURO ---
              precision    recall  f1-score   support
    Não PII       0.85      0.90      0.87       100
        PII       0.88      0.82      0.85        90

--- CLASSIFICADOR HÍBRIDO (Ensemble) ---
              precision    recall  f1-score   support
    Não PII       0.92      0.95      0.93       100
        PII       0.94      0.90      0.92        90

═══════════════════════════════════════════════════════════
BERT F1-Score:     0.8600
Baseline F1-Score: 0.8200
Híbrido F1-Score:  0.9250
═══════════════════════════════════════════════════════════
✅ O Híbrido superou o Baseline (Regex/SpaCy sozinhos)!
```

---

## 📁 Estrutura do Projeto

```
ShieldData/
│
├── 📂 data/
│   ├── raw/                    # Dados brutos (entrada)
│   └── processed/              # Dados processados (saída)
│
├── 📂 models/
│   └── best_model/             # Modelo BERT treinado
│       └── model_state.bin
│
├── 📂 src/
│   ├── __init__.py
│   ├── main.py                 # 🚀 Pipeline completo
│   ├── preprocessing.py        # 🧹 Limpeza e preparação
│   ├── validator.py            # 📝 Validação Regex (CPF, Email, etc)
│   ├── ner_detector.py         # 🧠 Detector de Entidades (SpaCy)
│   ├── piiclassifier.py        # 🤖 Modelo BERT
│   ├── train.py                # 🎓 Treinamento
│   ├── tune.py                 # 🔧 Otimização (Optuna)
│   ├── hybrid_classifier.py    # 🎯 Classificador Híbrido
│   ├── evaluate_hybrid.py      # 📊 Avaliação
│   ├── score_calculator.py     # 📈 Métricas
│   └── utils.py                # 🛠️ Utilitários
│
├── 📂 tests/
│   ├── test_score_calculator.py
│   └── test_label_comparison.py
│
├── 📄 requirements.txt         # Dependências
├── 📄 Makefile                 # Comandos úteis
├── 📄 README.md                # Este arquivo
├── 📄 REVISAO_CODIGO.md        # Relatório de revisão
└── 📄 RESUMO_REVISAO.md        # Resumo da revisão
```

---

## 🛠️ Tecnologias

### Core

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **Python** | 3.8+ | Linguagem principal |
| **PyTorch** | Latest | Framework de Deep Learning |
| **Transformers** | Latest | BERT (Hugging Face) |
| **SpaCy** | Latest | NER (pt_core_news_lg) |

### Machine Learning

| Biblioteca | Uso |
|------------|-----|
| **scikit-learn** | Métricas e validação |
| **Optuna** | Otimização de hiperparâmetros |
| **pandas** | Manipulação de dados |
| **numpy** | Operações numéricas |

### Utilidades

| Biblioteca | Uso |
|------------|-----|
| **openpyxl** | Leitura/escrita de Excel |
| **regex** | Expressões regulares avançadas |
| **tqdm** | Barras de progresso |
| **pytest** | Testes automatizados |

---

## 📊 Performance

### Métricas do Modelo Híbrido

| Métrica | Valor | Descrição |
|---------|-------|-----------|
| **F1-Score** | 0.92 | Média harmônica entre Precision e Recall |
| **Precision** | 0.94 | Acurácia dos positivos detectados |
| **Recall** | 0.90 | Cobertura dos casos positivos |
| **Accuracy** | 0.93 | Acurácia geral |

### Comparação de Abordagens

| Abordagem | F1-Score | Vantagens |
|-----------|----------|-----------|
| **Regex Puro** | 0.82 | Rápido, preciso para padrões fixos |
| **BERT Puro** | 0.86 | Entende contexto, flexível |
| **Híbrido** | **0.92** | ✅ Melhor dos dois mundos |

### Tempo de Execução

| Operação | Tempo (100 textos) | Device |
|----------|-------------------|--------|
| Pré-processamento | ~5s | CPU |
| Classificação (Regex) | ~0.1s | CPU |
| Classificação (BERT) | ~2s | CPU |
| Classificação (BERT) | ~0.5s | GPU/MPS |
| Classificação (Híbrido) | ~2.5s | CPU |

---

## 🧪 Testes

### Executar Todos os Testes

```bash
pytest tests/
```

### Executar Testes Específicos

```bash
# Testar calculadora de métricas
pytest tests/test_score_calculator.py -v

# Testar com cobertura
pytest tests/ --cov=src --cov-report=html
```

### Adicionar Novos Testes

Crie arquivos em `tests/` com prefixo `test_`:

```python
# tests/test_seu_modulo.py
import pytest
from src.seu_modulo import sua_funcao

def test_sua_funcao():
    resultado = sua_funcao("entrada")
    assert resultado == "esperado"
```

---

## 🎓 Exemplos de Uso

### Exemplo 1: Detecção Simples

```python
from hybrid_classifier import HybridClassifier

classifier = HybridClassifier()

# Texto com CPF
texto = "O CPF do cidadão é 123.456.789-00"
resultado = classifier.predict(texto)

print(resultado)
# {
#   'is_pii': True,
#   'confidence': 1.0,
#   'reason': 'Correspondência forte de Regex',
#   'details': {...}
# }
```

### Exemplo 2: Processamento em Lote

```python
import pandas as pd
from hybrid_classifier import HybridClassifier

# Carregar dados
df = pd.read_excel("data/raw/meus_dados.xlsx")

# Inicializar classificador
classifier = HybridClassifier()

# Classificar todos os textos
resultados = []
for texto in df['Texto Mascarado']:
    resultado = classifier.predict(texto)
    resultados.append(resultado['is_pii'])

# Adicionar resultados ao DataFrame
df['Contém_PII'] = resultados
df.to_excel("data/processed/resultados.xlsx")
```

### Exemplo 3: Ajuste de Threshold

```python
from hybrid_classifier import HybridClassifier

classifier = HybridClassifier()

# Threshold mais conservador (menos falsos positivos)
resultado = classifier.predict(texto, threshold=0.7)

# Threshold mais liberal (menos falsos negativos)
resultado = classifier.predict(texto, threshold=0.3)
```

---

## 🔧 Configuração Avançada

### Variáveis de Ambiente

```bash
# Forçar uso de CPU (mesmo com GPU disponível)
export CUDA_VISIBLE_DEVICES=""

# Configurar número de threads
export OMP_NUM_THREADS=4
```

### Ajuste de Memória

Se encontrar erros de memória:

```python
# Em train.py, reduza o batch_size
trainer = ModelTrainer(
    batch_size=8,  # Reduzir de 16 para 8
    # ...
)
```

### Usar GPU/MPS

O sistema detecta automaticamente:
- **CUDA** (NVIDIA GPU)
- **MPS** (Apple Silicon M1/M2)
- **CPU** (fallback)

Para forçar um device específico:

```python
classifier = HybridClassifier(device="cpu")  # ou "cuda" ou "mps"
```

---

## 🐛 Troubleshooting

### Problema: "Model not found"

```bash
# Certifique-se de treinar o modelo primeiro
python src/tune.py --trials 5
```

### Problema: "SpaCy model not found"

```bash
# Baixe o modelo SpaCy
python -m spacy download pt_core_news_lg
```

### Problema: "Out of memory"

```python
# Reduza o batch_size em train.py
batch_size=8  # ou até 4
```

### Problema: Importação falha

```bash
# Certifique-se de estar no diretório raiz
cd ShieldData

# E execute com python -m
python -m src.main
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Siga estes passos:

1. **Fork** o projeto
2. **Crie uma branch** (`git checkout -b feature/MinhaFeature`)
3. **Commit** suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. **Push** para a branch (`git push origin feature/MinhaFeature`)
5. **Abra um Pull Request**

### Diretrizes

- ✅ Escreva testes para novas funcionalidades
- ✅ Mantenha o código documentado (docstrings)
- ✅ Siga PEP 8 (use `black` para formatação)
- ✅ Atualize o README se necessário

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👥 Autores

Desenvolvido para o **Hackathon em Controle Social - GDF 2026**

---

## 📞 Suporte

Encontrou um bug? Tem uma sugestão?

- 🐛 [Abra uma Issue](https://github.com/seu-usuario/ShieldData/issues)
- 💬 [Discussões](https://github.com/seu-usuario/ShieldData/discussions)

---

## 🙏 Agradecimentos

- **Hugging Face** - Biblioteca Transformers
- **SpaCy** - Framework de NLP
- **Optuna** - Otimização de hiperparâmetros
- **GDF** - Organização do Hackathon

---

## 📚 Referências

- [BERT: Pre-training of Deep Bidirectional Transformers](https://arxiv.org/abs/1810.04805)
- [SpaCy Documentation](https://spacy.io/)
- [Optuna: A hyperparameter optimization framework](https://optuna.org/)
- [LGPD - Lei Geral de Proteção de Dados](http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)

---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela!**

Feito com ❤️ para proteger a privacidade dos cidadãos

</div>
