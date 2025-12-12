# 🚀 Guia Completo: Pipeline GitLab CI/CD

## 📋 Índice
1. [Visão Geral](#visão-geral)
2. [Pré-requisitos](#pré-requisitos)
3. [Estrutura do Pipeline](#estrutura-do-pipeline)
4. [Passo a Passo Detalhado](#passo-a-passo-detalhado)
5. [Como Deixar o Pipeline Verde](#como-deixar-o-pipeline-verde)
6. [Troubleshooting](#troubleshooting)
7. [Badges e Métricas](#badges-e-métricas)

---

## 🎯 Visão Geral

Este projeto implementa um **pipeline CI/CD completo** com 4 stages:

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│   LINT   │ -> │   TEST   │ -> │ SECURITY │ -> │  DEPLOY  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
```

### Camadas de Qualidade Implementadas

✅ **Linting:** flake8, pylint, black, radon  
✅ **Testes:** pytest com coverage  
✅ **Segurança:** bandit, safety  
✅ **Deploy:** staging e production  

---

## 📦 Pré-requisitos

### 1. Conta no GitLab
- Acesse: https://gitlab.com
- Crie uma conta gratuita (se não tiver)
- Verifique seu email

### 2. Arquivos Necessários no Projeto

```
casseb2310/
├── .gitlab-ci.yml           ✅ Pipeline CI/CD
├── requirements-dev.txt     ✅ Dependências de dev
├── requirements.txt         ✅ Dependências de produção
├── .flake8                  ✅ Config Flake8
├── .pylintrc                ✅ Config Pylint
├── pyproject.toml           ✅ Config Black/Pytest
├── test_produto_manager.py  ✅ Testes unitários
├── test_app.py              ✅ Testes de integração
├── app.py                   ✅ Aplicação
└── produto_manager.py       ✅ Módulo principal
```

---

## 🏗️ Estrutura do Pipeline

### Stage 1️⃣: LINT (Qualidade de Código)

| Job | Ferramenta | Propósito | Crítico |
|-----|------------|-----------|---------|
| `flake8` | Flake8 | Verifica PEP8 e erros de sintaxe | ✅ Sim |
| `pylint` | Pylint | Análise estática avançada | ⚠️ Não |
| `black-check` | Black | Verifica formatação | ⚠️ Não |
| `code-quality` | Radon | Complexidade e manutenibilidade | ⚠️ Não |

### Stage 2️⃣: TEST (Testes)

| Job | Ferramenta | Propósito | Crítico |
|-----|------------|-----------|---------|
| `unit-tests` | Pytest | Testes unitários + coverage | ✅ Sim |
| `integration-tests` | Pytest | Testes de integração | ⚠️ Não |
| `generate-badge` | Anybadge | Gera badges de status | ⚠️ Não |

### Stage 3️⃣: SECURITY (Segurança)

| Job | Ferramenta | Propósito | Crítico |
|-----|------------|-----------|---------|
| `safety-check` | Safety | Vulnerabilidades em dependências | ⚠️ Não |
| `bandit` | Bandit | Problemas de segurança no código | ⚠️ Não |

### Stage 4️⃣: DEPLOY (Implantação)

| Job | Ambiente | Quando | Crítico |
|-----|----------|--------|---------|
| `deploy-staging` | Staging | Branch `develop` | ⚠️ Não |
| `deploy-production` | Production | Branch `main/master` | ⚠️ Não |

---

## 📝 Passo a Passo Detalhado

### Etapa 1: Criar Repositório no GitLab

1. **Acesse GitLab:**
   ```
   https://gitlab.com
   ```

2. **Crie um Novo Projeto:**
   - Clique em **"New project"**
   - Selecione **"Create blank project"**
   - **Project name:** `sistema-produtos`
   - **Visibility:** Public ou Private
   - ✅ **Initialize repository with a README:** NÃO marcar
   - Clique em **"Create project"**

3. **Anote a URL do repositório:**
   ```
   https://gitlab.com/seu-usuario/sistema-produtos.git
   ```

### Etapa 2: Configurar Git Localmente

Abra o terminal no diretório do projeto:

```bash
cd /c/Users/ronal/Downloads/casseb2310

# Verificar repositório atual
git remote -v

# Remover remote do GitHub (se existir)
git remote remove origin

# Adicionar remote do GitLab
git remote add origin https://gitlab.com/SEU-USUARIO/sistema-produtos.git

# Verificar configuração
git remote -v
```

### Etapa 3: Fazer Push para GitLab

```bash
# Adicionar todos os arquivos novos
git add .

# Fazer commit
git commit -m "feat: Adiciona pipeline CI/CD com linting, testes e segurança"

# Renomear branch para main (se necessário)
git branch -M main

# Push para GitLab
git push -u origin main
```

**Primeira vez?** Configure suas credenciais:
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

### Etapa 4: Acompanhar o Pipeline

1. **Acesse seu projeto no GitLab**
2. No menu lateral, clique em **"CI/CD" → "Pipelines"**
3. Você verá o pipeline executando

**Status possíveis:**
- 🔵 **Running:** Em execução
- 🟢 **Passed:** Sucesso! ✅
- 🔴 **Failed:** Falhou (veja os logs)
- ⚪ **Pending:** Aguardando

### Etapa 5: Verificar Jobs Individuais

1. Clique no pipeline em execução
2. Veja cada job:
   - ✅ Verde = Passou
   - ❌ Vermelho = Falhou
   - ⏭️ Pulado = Não executado
3. Clique em um job para ver os logs

---

## ✅ Como Deixar o Pipeline Verde

### Problema Comum 1: Flake8 Falha

**Erro:**
```
app.py:10:80: E501 line too long (105 > 100 characters)
```

**Solução:**
```bash
# Verificar erros localmente
flake8 app.py produto_manager.py

# Corrigir automaticamente com black
black app.py produto_manager.py

# Verificar novamente
flake8 app.py produto_manager.py
```

### Problema Comum 2: Testes Falham

**Erro:**
```
FAILED test_produto_manager.py::test_adicionar_produto
```

**Solução:**
```bash
# Executar testes localmente
pytest -v

# Ver qual teste falhou e corrigir o código
# Executar novamente até passar
pytest -v
```

### Problema Comum 3: Coverage Baixo

**Erro:**
```
Coverage: 65% (mínimo recomendado: 80%)
```

**Solução:**
- Adicione mais testes para cobrir código não testado
- Veja relatório: `pytest --cov=. --cov-report=html`
- Abra `htmlcov/index.html` no navegador

### Checklist para Pipeline Verde ✅

Execute localmente ANTES de fazer push:

```bash
# 1. Formatar código
black app.py produto_manager.py test_*.py

# 2. Verificar linting
flake8 app.py produto_manager.py

# 3. Executar testes
pytest -v

# 4. Verificar coverage
pytest --cov=. --cov-report=term-missing

# 5. Se tudo passar, commit e push
git add .
git commit -m "fix: Corrige problemas de linting e testes"
git push origin main
```

---

## 🐛 Troubleshooting

### Pipeline não inicia

**Problema:** Pipeline não aparece após o push

**Solução:**
1. Verifique se `.gitlab-ci.yml` existe na raiz do projeto
2. Verifique se o arquivo tem sintaxe YAML correta
3. Acesse: **CI/CD → Editor** para validar

### Job fica em "Pending" muito tempo

**Problema:** Job não executa

**Solução:**
- GitLab Free tem limite de runners compartilhados
- Aguarde alguns minutos
- Ou configure um GitLab Runner próprio

### Erro: "requirements-dev.txt not found"

**Problema:** Arquivo de dependências não encontrado

**Solução:**
```bash
# Certifique-se que o arquivo existe
ls requirements-dev.txt

# Adicione ao git
git add requirements-dev.txt
git commit -m "fix: Adiciona requirements-dev.txt"
git push
```

### Erro de Importação nos Testes

**Problema:**
```
ImportError: No module named 'flask'
```

**Solução:**
- Verifique se `requirements-dev.txt` inclui todas as dependências
- O pipeline instala automaticamente antes de executar

### Quer Ver Logs Detalhados

```bash
# No job que falhou, clique em:
# - "Show complete raw" (para ver log completo)
# - "Download" (para baixar log)
```

---

## 🏅 Badges e Métricas

### Adicionar Badge ao README

No GitLab, acesse: **Settings → CI/CD → General pipelines**

Copie o código Markdown:
```markdown
[![pipeline status](https://gitlab.com/SEU-USUARIO/sistema-produtos/badges/main/pipeline.svg)](https://gitlab.com/SEU-USUARIO/sistema-produtos/-/commits/main)

[![coverage report](https://gitlab.com/SEU-USUARIO/sistema-produtos/badges/main/coverage.svg)](https://gitlab.com/SEU-USUARIO/sistema-produtos/-/commits/main)
```

### Métricas Disponíveis

No GitLab você pode ver:
- 📊 **Pipeline history:** Histórico de execuções
- 📈 **Coverage trends:** Tendência de cobertura
- ⏱️ **Duration:** Tempo de execução
- 📉 **Success rate:** Taxa de sucesso

---

## 🎓 Conceitos Importantes

### CI/CD (Continuous Integration/Continuous Deployment)

**Continuous Integration (CI):**
- Integração contínua de código
- Testes automáticos em cada commit
- Detecção precoce de bugs

**Continuous Deployment (CD):**
- Deploy automático após testes passarem
- Entrega rápida de features
- Redução de erros em produção

### Stages (Etapas)

Cada stage agrupa jobs relacionados:
- **Jobs do mesmo stage:** Executam em paralelo
- **Stages diferentes:** Executam em sequência
- **Se um stage falha:** Próximos não executam

### Jobs

Cada job é uma tarefa específica:
- Executa em ambiente isolado
- Pode ter artefatos (arquivos gerados)
- Pode ter allow_failure (não crítico)

---

## 📚 Referências

- **GitLab CI/CD:** https://docs.gitlab.com/ee/ci/
- **Pytest:** https://docs.pytest.org/
- **Flake8:** https://flake8.pycqa.org/
- **Black:** https://black.readthedocs.io/

---

## 🎯 Resumo dos Comandos

### Configurar e Enviar para GitLab
```bash
git remote add origin https://gitlab.com/SEU-USUARIO/sistema-produtos.git
git add .
git commit -m "feat: Adiciona pipeline CI/CD"
git push -u origin main
```

### Testar Localmente (antes do push)
```bash
# Instalar dependências de dev
pip install -r requirements-dev.txt

# Formatar código
black app.py produto_manager.py test_*.py

# Linting
flake8 app.py produto_manager.py

# Testes
pytest -v --cov=.

# Se tudo OK, push!
git push origin main
```

### Ver Status do Pipeline
```bash
# Via web
# https://gitlab.com/SEU-USUARIO/sistema-produtos/-/pipelines

# Ou instale o GitLab CLI
# https://gitlab.com/gitlab-org/cli
```

---

## ✅ Checklist Final

Antes de enviar para o professor:

- [ ] Repositório criado no GitLab
- [ ] Código enviado com `git push`
- [ ] Pipeline executando (azul ou verde)
- [ ] Todos os jobs críticos passando (verde)
- [ ] Badge do pipeline no README (opcional mas bonito!)
- [ ] Link do GitLab pronto para enviar

**Link para enviar:**
```
https://gitlab.com/SEU-USUARIO/sistema-produtos
```

---

## 🎉 Parabéns!

Se seguiu todos os passos, seu pipeline está verde! ✅

**O que isso significa:**
- ✅ Código segue boas práticas (linting)
- ✅ Testes passando com boa cobertura
- ✅ Sem vulnerabilidades de segurança
- ✅ Pronto para deploy em produção

---

**Data de criação:** 12/12/2025  
**Atividade:** 6 - Pipeline CI/CD  
**Status:** ✅ Pronto para entrega
