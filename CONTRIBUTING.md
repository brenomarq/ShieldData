# 🤝 Guia de Contribuição - ShieldData

Obrigado por considerar contribuir com o ShieldData! Este documento fornece diretrizes para contribuir com o projeto.

---

## 📋 Índice

- [Código de Conduta](#-código-de-conduta)
- [Como Contribuir](#-como-contribuir)
- [Reportando Bugs](#-reportando-bugs)
- [Sugerindo Melhorias](#-sugerindo-melhorias)
- [Desenvolvimento](#-desenvolvimento)
- [Padrões de Código](#-padrões-de-código)
- [Processo de Pull Request](#-processo-de-pull-request)

---

## 📜 Código de Conduta

Este projeto adere a um código de conduta. Ao participar, espera-se que você mantenha este código:

- ✅ Seja respeitoso e inclusivo
- ✅ Aceite críticas construtivas
- ✅ Foque no que é melhor para a comunidade
- ✅ Mostre empatia com outros membros

---

## 🚀 Como Contribuir

Existem várias formas de contribuir:

### 1. Reportar Bugs 🐛
Encontrou um bug? [Abra uma issue](https://github.com/seu-usuario/ShieldData/issues/new)

### 2. Sugerir Funcionalidades 💡
Tem uma ideia? [Abra uma discussão](https://github.com/seu-usuario/ShieldData/discussions)

### 3. Melhorar Documentação 📚
Documentação nunca é demais! Correções e melhorias são sempre bem-vindas.

### 4. Contribuir com Código 💻
Veja a seção [Desenvolvimento](#-desenvolvimento) abaixo.

---

## 🐛 Reportando Bugs

Ao reportar um bug, inclua:

### Informações Essenciais

```markdown
**Descrição do Bug**
Uma descrição clara e concisa do bug.

**Como Reproduzir**
Passos para reproduzir o comportamento:
1. Execute '...'
2. Com os dados '...'
3. Veja o erro

**Comportamento Esperado**
O que você esperava que acontecesse.

**Comportamento Atual**
O que realmente aconteceu.

**Screenshots**
Se aplicável, adicione screenshots.

**Ambiente:**
 - OS: [e.g. macOS 13.0]
 - Python: [e.g. 3.10.5]
 - Versão do ShieldData: [e.g. 1.0.0]

**Informações Adicionais**
Qualquer outro contexto sobre o problema.
```

---

## 💡 Sugerindo Melhorias

Ao sugerir uma melhoria, inclua:

- **Problema que resolve:** Qual problema sua sugestão resolve?
- **Solução proposta:** Como você sugere resolver?
- **Alternativas:** Quais alternativas você considerou?
- **Contexto adicional:** Screenshots, exemplos, etc.

---

## 🛠️ Desenvolvimento

### Configuração do Ambiente

```bash
# 1. Fork o repositório no GitHub

# 2. Clone seu fork
git clone https://github.com/SEU-USUARIO/ShieldData.git
cd ShieldData

# 3. Adicione o repositório original como upstream
git remote add upstream https://github.com/USUARIO-ORIGINAL/ShieldData.git

# 4. Crie um ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 5. Instale dependências de desenvolvimento
make install-dev

# 6. Crie uma branch para sua feature
git checkout -b feature/minha-feature
```

### Estrutura de Branches

- `main` - Branch principal (estável)
- `develop` - Branch de desenvolvimento
- `feature/*` - Novas funcionalidades
- `bugfix/*` - Correções de bugs
- `hotfix/*` - Correções urgentes
- `docs/*` - Melhorias de documentação

### Workflow de Desenvolvimento

```bash
# 1. Certifique-se de estar atualizado
git checkout develop
git pull upstream develop

# 2. Crie sua branch
git checkout -b feature/minha-feature

# 3. Faça suas alterações
# ... código ...

# 4. Execute os testes
make test

# 5. Formate o código
make format

# 6. Verifique o estilo
make lint

# 7. Commit suas mudanças
git add .
git commit -m "feat: adiciona minha feature"

# 8. Push para seu fork
git push origin feature/minha-feature

# 9. Abra um Pull Request no GitHub
```

---

## 📏 Padrões de Código

### Python Style Guide

Seguimos [PEP 8](https://pep8.org/) com algumas adaptações:

```python
# ✅ BOM
def calcular_f1_score(y_true: list, y_pred: list) -> float:
    """
    Calcula o F1-Score.
    
    Args:
        y_true: Rótulos verdadeiros
        y_pred: Rótulos previstos
    
    Returns:
        F1-Score calculado
    """
    # Implementação...
    return f1_score

# ❌ RUIM
def calc(a,b):
    return f1_score(a,b)
```

### Convenções

#### Nomenclatura

```python
# Classes: PascalCase
class HybridClassifier:
    pass

# Funções e variáveis: snake_case
def processar_texto(texto_entrada: str) -> str:
    resultado_processado = limpar_texto(texto_entrada)
    return resultado_processado

# Constantes: UPPER_SNAKE_CASE
BERT_HIGH_CONFIDENCE_THRESHOLD = 0.8
DEFAULT_BATCH_SIZE = 16
```

#### Docstrings

Use docstrings no estilo Google:

```python
def minha_funcao(param1: str, param2: int) -> bool:
    """
    Descrição breve da função.
    
    Descrição mais detalhada se necessário.
    
    Args:
        param1: Descrição do primeiro parâmetro
        param2: Descrição do segundo parâmetro
    
    Returns:
        Descrição do retorno
    
    Raises:
        ValueError: Quando param2 é negativo
    
    Example:
        >>> minha_funcao("teste", 5)
        True
    """
    if param2 < 0:
        raise ValueError("param2 deve ser positivo")
    return True
```

#### Type Hints

Sempre use type hints:

```python
# ✅ BOM
def processar(texto: str, threshold: float = 0.5) -> dict[str, Any]:
    pass

# ❌ RUIM
def processar(texto, threshold=0.5):
    pass
```

### Formatação Automática

```bash
# Formatar código com black
make format

# Verificar estilo com flake8
make lint

# Type checking com mypy
make typecheck
```

### Testes

Todo código novo deve ter testes:

```python
# tests/test_meu_modulo.py
import pytest
from src.meu_modulo import minha_funcao

def test_minha_funcao_caso_basico():
    """Testa caso básico."""
    resultado = minha_funcao("entrada")
    assert resultado == "esperado"

def test_minha_funcao_caso_erro():
    """Testa tratamento de erro."""
    with pytest.raises(ValueError):
        minha_funcao("entrada_invalida")

def test_minha_funcao_casos_extremos():
    """Testa casos extremos."""
    assert minha_funcao("") == ""
    assert minha_funcao(None) is None
```

Executar testes:

```bash
# Todos os testes
make test

# Com cobertura
make test-coverage

# Específico
pytest tests/test_meu_modulo.py -v
```

---

## 🔄 Processo de Pull Request

### Checklist Antes de Submeter

- [ ] Código segue os padrões do projeto
- [ ] Comentários em português
- [ ] Docstrings adicionadas/atualizadas
- [ ] Testes adicionados/atualizados
- [ ] Todos os testes passam (`make test`)
- [ ] Código formatado (`make format`)
- [ ] Sem erros de lint (`make lint`)
- [ ] README atualizado (se necessário)
- [ ] CHANGELOG atualizado (se necessário)

### Mensagens de Commit

Seguimos [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Formato
<tipo>(<escopo>): <descrição>

[corpo opcional]

[rodapé opcional]
```

#### Tipos

- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Apenas documentação
- `style`: Formatação, sem mudança de código
- `refactor`: Refatoração de código
- `perf`: Melhoria de performance
- `test`: Adição/correção de testes
- `chore`: Tarefas de manutenção

#### Exemplos

```bash
# Feature
git commit -m "feat(classifier): adiciona suporte para RG"

# Bug fix
git commit -m "fix(validator): corrige validação de CPF com zeros"

# Documentação
git commit -m "docs(readme): atualiza exemplos de uso"

# Refatoração
git commit -m "refactor(utils): extrai função get_best_device"

# Performance
git commit -m "perf(ner): otimiza processamento em lote"
```

### Template de Pull Request

```markdown
## Descrição
Descrição clara do que este PR faz.

## Tipo de Mudança
- [ ] Bug fix (correção que resolve um problema)
- [ ] Nova feature (adiciona funcionalidade)
- [ ] Breaking change (mudança que quebra compatibilidade)
- [ ] Documentação

## Como Testar
1. Execute `...`
2. Verifique `...`
3. Confirme que `...`

## Checklist
- [ ] Código segue os padrões do projeto
- [ ] Testes adicionados/atualizados
- [ ] Todos os testes passam
- [ ] Documentação atualizada
- [ ] Sem warnings de lint

## Screenshots (se aplicável)
Adicione screenshots se relevante.

## Issues Relacionadas
Closes #123
Refs #456
```

### Revisão de Código

Seu PR será revisado por mantenedores. Espere:

1. **Feedback construtivo** - Sugestões de melhoria
2. **Discussão** - Esclarecimentos sobre decisões
3. **Aprovação** - Quando tudo estiver OK
4. **Merge** - Integração ao projeto

---

## 🎯 Áreas que Precisam de Ajuda

Procurando por onde começar? Estas áreas precisam de contribuições:

### 🟢 Bom para Iniciantes

- [ ] Melhorar documentação
- [ ] Adicionar mais exemplos
- [ ] Corrigir typos
- [ ] Adicionar testes unitários

### 🟡 Nível Intermediário

- [ ] Otimizar performance
- [ ] Adicionar novos validadores (CNH, PIS, etc)
- [ ] Melhorar tratamento de erros
- [ ] Adicionar logging mais detalhado

### 🔴 Nível Avançado

- [ ] Implementar cache de predições
- [ ] Refatorar timeout no validator
- [ ] Adicionar suporte para outros idiomas
- [ ] Implementar API REST

---

## 📞 Precisa de Ajuda?

- 💬 [Discussões](https://github.com/seu-usuario/ShieldData/discussions)
- 📧 Email: seu-email@exemplo.com
- 🐛 [Issues](https://github.com/seu-usuario/ShieldData/issues)

---

## 🙏 Agradecimentos

Obrigado por contribuir com o ShieldData! Sua ajuda é muito apreciada. 🎉

---

**Lembre-se:** Não existe contribuição pequena demais. Toda ajuda é bem-vinda!
