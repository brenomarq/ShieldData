# Makefile para ShieldData
# Comandos úteis para desenvolvimento e uso do projeto

.PHONY: help install install-dev test clean process train tune evaluate examples run-all

# Comando padrão: mostrar ajuda
help:
	@echo "🛡️  ShieldData - Comandos Disponíveis"
	@echo ""
	@echo "📦 Instalação:"
	@echo "  make install        - Instalar dependências e modelo SpaCy"
	@echo "  make install-dev    - Instalar dependências de desenvolvimento"
	@echo ""
	@echo "🚀 Execução:"
	@echo "  make run-all        - Executar pipeline completo (processo + treino)"
	@echo "  make process        - Pré-processar dados"
	@echo "  make train          - Treinar modelo BERT"
	@echo "  make tune           - Otimizar hiperparâmetros (Optuna)"
	@echo "  make evaluate       - Avaliar modelo híbrido"
	@echo "  make examples       - Executar exemplos práticos"
	@echo ""
	@echo "🧪 Testes:"
	@echo "  make test           - Executar todos os testes"
	@echo "  make test-verbose   - Executar testes com output detalhado"
	@echo "  make test-coverage  - Executar testes com cobertura"
	@echo ""
	@echo "🧹 Limpeza:"
	@echo "  make clean          - Limpar arquivos cache"
	@echo "  make clean-all      - Limpar cache e modelos"
	@echo ""
	@echo "📊 Informações:"
	@echo "  make info           - Mostrar informações do ambiente"
	@echo "  make check          - Verificar instalação"

# Instalação básica
install:
	@echo "📦 Instalando dependências..."
	pip install -r requirements.txt
	@echo "🧠 Baixando modelo SpaCy (pt_core_news_lg)..."
	python3 -m spacy download pt_core_news_lg
	@echo "✅ Instalação concluída!"

# Instalação para desenvolvimento
install-dev:
	@echo "📦 Instalando dependências de desenvolvimento..."
	pip install -r requirements.txt
	pip install black flake8 mypy pytest-cov ipython jupyter
	python3 -m spacy download pt_core_news_lg
	@echo "✅ Instalação de desenvolvimento concluída!"

# Executar pipeline completo
run-all:
	@echo "🚀 Executando pipeline completo..."
	python3 src/main.py

# Pré-processamento
process:
	@echo "🧹 Pré-processando dados..."
	python3 src/preprocessing.py \
		--input "data/raw/AMOSTRA_e-SIC.xlsx" \
		--output "data/processed/AMOSTRA_e-SIC_processed.xlsx"

# Treinamento simples
train:
	@echo "🎓 Treinando modelo BERT..."
	python3 src/train.py

# Otimização de hiperparâmetros
tune:
	@echo "🔧 Otimizando hiperparâmetros com Optuna..."
	python3 src/tune.py --trials 10

# Otimização rápida (menos trials)
tune-fast:
	@echo "🔧 Otimização rápida (5 trials)..."
	python3 src/tune.py --trials 5

# Avaliação do modelo híbrido
evaluate:
	@echo "📊 Avaliando modelo híbrido..."
	python3 src/evaluate_hybrid.py

# Executar exemplos práticos
examples:
	@echo "💡 Executando exemplos práticos..."
	python3 examples.py

# Testes
test:
	@echo "🧪 Executando testes..."
	pytest tests/

# Testes com output detalhado
test-verbose:
	@echo "🧪 Executando testes (verbose)..."
	pytest tests/ -v

# Testes com cobertura
test-coverage:
	@echo "🧪 Executando testes com cobertura..."
	pytest tests/ --cov=src --cov-report=html --cov-report=term
	@echo "📊 Relatório de cobertura gerado em htmlcov/index.html"

# Limpeza de cache
clean:
	@echo "🧹 Limpando arquivos cache..."
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf tests/__pycache__
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "✅ Cache limpo!"

# Limpeza completa (incluindo modelos)
clean-all: clean
	@echo "🧹 Limpando modelos treinados..."
	rm -rf models/trial_*
	@echo "⚠️  Mantendo models/best_model (delete manualmente se necessário)"
	@echo "✅ Limpeza completa!"

# Informações do ambiente
info:
	@echo "📊 Informações do Ambiente:"
	@echo ""
	@echo "Python:"
	@python3 --version
	@echo ""
	@echo "Pip:"
	@pip --version
	@echo ""
	@echo "PyTorch:"
	@python3 -c "import torch; print(f'  Versão: {torch.__version__}'); print(f'  CUDA disponível: {torch.cuda.is_available()}'); print(f'  MPS disponível: {torch.backends.mps.is_available() if hasattr(torch.backends, \"mps\") else False}')" 2>/dev/null || echo "  Não instalado"
	@echo ""
	@echo "SpaCy:"
	@python3 -c "import spacy; print(f'  Versão: {spacy.__version__}')" 2>/dev/null || echo "  Não instalado"

# Verificar instalação
check:
	@echo "🔍 Verificando instalação..."
	@echo ""
	@echo "1. Verificando Python..."
	@python3 --version || (echo "❌ Python não encontrado" && exit 1)
	@echo "✅ Python OK"
	@echo ""
	@echo "2. Verificando dependências..."
	@python3 -c "import pandas, numpy, sklearn, spacy, transformers, torch, openpyxl, pytest, optuna" && echo "✅ Todas as dependências instaladas" || (echo "❌ Faltam dependências. Execute: make install" && exit 1)
	@echo ""
	@echo "3. Verificando modelo SpaCy..."
	@python3 -c "import spacy; spacy.load('pt_core_news_lg')" && echo "✅ Modelo SpaCy OK" || (echo "❌ Modelo SpaCy não encontrado. Execute: python3 -m spacy download pt_core_news_lg" && exit 1)
	@echo ""
	@echo "4. Verificando estrutura de diretórios..."
	@test -d data/raw && echo "✅ data/raw/ existe" || echo "⚠️  data/raw/ não encontrado"
	@test -d data/processed && echo "✅ data/processed/ existe" || echo "⚠️  data/processed/ não encontrado"
	@test -d models && echo "✅ models/ existe" || echo "⚠️  models/ não encontrado"
	@echo ""
	@echo "✅ Verificação concluída!"

# Formatar código com black
format:
	@echo "🎨 Formatando código com black..."
	black src/ tests/ examples.py
	@echo "✅ Código formatado!"

# Verificar estilo com flake8
lint:
	@echo "🔍 Verificando estilo com flake8..."
	flake8 src/ tests/ examples.py --max-line-length=120
	@echo "✅ Estilo verificado!"

# Type checking com mypy
typecheck:
	@echo "🔍 Verificando tipos com mypy..."
	mypy src/ --ignore-missing-imports
	@echo "✅ Tipos verificados!"
