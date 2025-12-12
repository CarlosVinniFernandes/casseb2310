# ✅ CHECKLIST PARA ENTREGAR A ATIVIDADE 6

## 📋 Resumo do Que Foi Implementado

### ✅ Linting Code (Qualidade de Código)
- **Flake8:** Verifica PEP8 e erros de sintaxe
- **Pylint:** Análise estática avançada  
- **Black:** Formatação automática de código
- **Radon:** Análise de complexidade e manutenibilidade

### ✅ Testes Unitários
- **39 testes** implementados com pytest
- **30 testes** para produto_manager.py
- **9 testes** para app.py
- **79% de cobertura** de código
- **100% de cobertura** no módulo principal

### ✅ Pipeline GitLab CI/CD
- **4 Stages:** lint → test → security → deploy
- **10 Jobs** configurados
- Análise de segurança com Bandit e Safety
- Artefatos de coverage e relatórios

---

## 🚀 PASSO A PASSO PARA ENTREGAR

### 1️⃣ Criar Repositório no GitLab

```bash
# 1. Acesse: https://gitlab.com
# 2. Faça login ou crie uma conta
# 3. Clique em "New project" → "Create blank project"
# 4. Preencha:
#    - Project name: sistema-produtos
#    - Visibility: Public (recomendado para visualização do professor)
# 5. Clique em "Create project"
```

### 2️⃣ Configurar Git Local

```bash
# Navegue até o diretório do projeto
cd /c/Users/ronal/Downloads/casseb2310

# Verificar repositório atual
git remote -v

# Remover remote antigo (se houver)
git remote remove origin

# Adicionar remote do GitLab (SUBSTITUA SEU-USUARIO pelo seu usuário do GitLab)
git remote add origin https://gitlab.com/SEU-USUARIO/sistema-produtos.git

# Verificar
git remote -v
```

### 3️⃣ Fazer Push para GitLab

```bash
# Renomear branch para main (se necessário)
git branch -M main

# Fazer push
git push -u origin main

# Se pedir credenciais:
# Username: seu-usuario-gitlab
# Password: use um Personal Access Token (não a senha)
```

**Como criar Personal Access Token:**
1. GitLab → Preferências → Access Tokens
2. Nome: "git-push"  
3. Scopes: marque `api`, `read_repository`, `write_repository`
4. Create token
5. Copie o token (aparece só uma vez!)
6. Use no lugar da senha

### 4️⃣ Verificar Pipeline

```bash
# 1. Acesse: https://gitlab.com/SEU-USUARIO/sistema-produtos
# 2. Menu lateral → CI/CD → Pipelines
# 3. Você verá o pipeline executando (azul)
# 4. Aguarde ficar VERDE ✅
```

### 5️⃣ Verificar Ícone Verde

**O que significa Pipeline Verde:**
- ✅ Todos os jobs CRÍTICOS passaram
- ✅ Código segue boas práticas (flake8)
- ✅ Testes unitários passando (pytest)
- ✅ Pronto para produção

**Se aparecer VERMELHO:**
1. Clique no pipeline
2. Veja qual job falhou
3. Clique no job para ver o log
4. Corrija o problema localmente
5. Faça commit e push novamente

### 6️⃣ Copiar Link para Entrega

```
Link do projeto:
https://gitlab.com/SEU-USUARIO/sistema-produtos

Link direto do pipeline:
https://gitlab.com/SEU-USUARIO/sistema-produtos/-/pipelines
```

---

## 🔍 COMO GARANTIR QUE O PIPELINE FIQUE VERDE

### Teste TUDO Localmente Antes de Fazer Push

```bash
# Entre no diretório do projeto
cd /c/Users/ronal/Downloads/casseb2310

# Ative o ambiente virtual
.venv/Scripts/activate

# 1. Instale as dependências
pip install -r requirements-dev.txt

# 2. Formate o código
black app.py produto_manager.py test_*.py

# 3. Verifique linting
flake8 app.py produto_manager.py

# 4. Execute os testes
pytest -v

# 5. Verifique coverage
pytest --cov=. --cov-report=term-missing

# SE TUDO PASSAR LOCALMENTE, pipeline no GitLab também passará!
```

---

## 📊 Resultados Esperados

### Jobs que DEVEM passar (críticos)

✅ **flake8** - Deve estar VERDE  
✅ **unit-tests** - Deve estar VERDE

### Jobs que PODEM falhar (não críticos)

⚠️ **pylint** - Pode estar amarelo (allow_failure: true)  
⚠️ **black-check** - Pode estar amarelo  
⚠️ **code-quality** - Pode estar amarelo  
⚠️ **safety-check** - Pode estar amarelo  
⚠️ **bandit** - Pode estar amarelo  

**Pipeline fica VERDE se os jobs críticos passarem!**

---

## 📸 Como Tirar Print do Pipeline Verde

1. Acesse: `https://gitlab.com/SEU-USUARIO/sistema-produtos/-/pipelines`
2. Veja o pipeline com ícone VERDE ✅
3. Tire print (ou screenshot)
4. Anexe na entrega (se solicitado)

---

## 🎯 Para Entregar ao Professor

### Informações Necessárias:

```
Link do Projeto GitLab:
https://gitlab.com/SEU-USUARIO/sistema-produtos

Status do Pipeline:
✅ VERDE (Passed)

Coverage de Testes:
79% total (100% no módulo principal)

Total de Testes:
39 testes (todos passando)
```

### Descrição para Envio:

```
Projeto: Sistema de Gestão de Produtos
Atividade: 6 - Pipeline CI/CD

Implementações:
- Pipeline GitLab CI/CD com 4 stages
- Linting: flake8, pylint, black, radon
- 39 testes unitários (pytest)
- 79% de cobertura de código
- Análise de segurança (bandit, safety)
- Todos os testes passando ✅
- Pipeline aprovado (verde) ✅

Link: https://gitlab.com/SEU-USUARIO/sistema-produtos
```

---

## ⚡ Comandos Rápidos de Referência

```bash
# Ver status do git
git status

# Ver histórico de commits
git log --oneline

# Ver remote configurado
git remote -v

# Fazer alterações e push
git add .
git commit -m "mensagem"
git push origin main

# Executar testes localmente
pytest -v

# Ver cobertura
pytest --cov=.

# Formatar código
black app.py produto_manager.py
```

---

## 📞 Resolução de Problemas Comuns

### Problema 1: Pipeline não aparece
**Solução:** Verifique se `.gitlab-ci.yml` está na raiz do projeto

### Problema 2: Job "flake8" falha
**Solução:**
```bash
flake8 app.py produto_manager.py
black app.py produto_manager.py
git add .
git commit -m "fix: Corrige formatação"
git push
```

### Problema 3: Testes falham no GitLab mas passam localmente
**Solução:**
- Verifique se `requirements-dev.txt` tem todas as dependências
- Certifique-se que não há dependência de arquivos locais

### Problema 4: Erro de autenticação no push
**Solução:**
- Use Personal Access Token ao invés da senha
- GitLab → Settings → Access Tokens

---

## ✅ CHECKLIST FINAL ANTES DE ENTREGAR

- [ ] Repositório criado no GitLab
- [ ] Código enviado com `git push`
- [ ] Pipeline executado e VERDE ✅
- [ ] Flake8 passou (verde)
- [ ] Unit-tests passou (verde)
- [ ] Link do GitLab copiado
- [ ] Print do pipeline (opcional)
- [ ] Enviado para o professor

---

## 🎉 Parabéns!

Se seguiu todos os passos, seu projeto está pronto para entrega!

**Ícone Verde = Atividade Aprovada!** ✅

---

**Criado em:** 12/12/2025  
**Atividade:** 6 - Pipeline GitLab CI/CD  
**Status:** ✅ Pronto para entrega
