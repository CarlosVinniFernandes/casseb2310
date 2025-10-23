# 🚀 Guia de Deploy no Render

## Passo a Passo Detalhado

### 1️⃣ Preparar o Repositório no GitHub

1. Crie um novo repositório no GitHub (público ou privado)
2. No terminal do projeto, adicione o remote:

```bash
git remote add origin https://github.com/seu-usuario/sistema-produtos.git
git branch -M main
git push -u origin main
```

### 2️⃣ Criar Conta no Render

1. Acesse: https://render.com
2. Clique em "Get Started for Free"
3. Faça login com GitHub (recomendado) ou crie uma conta

### 3️⃣ Criar um Web Service

1. No Dashboard do Render, clique em **"New +"**
2. Selecione **"Web Service"**
3. Conecte seu repositório GitHub:
   - Se for a primeira vez, autorize o Render a acessar o GitHub
   - Selecione o repositório `sistema-produtos`

### 4️⃣ Configurar o Web Service

Preencha os seguintes campos:

**Configurações Básicas:**
- **Name:** `sistema-produtos` (ou outro nome de sua preferência)
- **Region:** Escolha a região mais próxima (ex: Oregon, Ohio)
- **Branch:** `main`
- **Root Directory:** (deixe em branco)
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`

**Plano:**
- **Instance Type:** Selecione **Free** (grátis)
  - ⚠️ Nota: O plano Free "dorme" após 15 minutos de inatividade e demora ~30 segundos para "acordar"

**Variáveis de Ambiente (Opcional mas Recomendado):**

Clique em "Advanced" e adicione:
- **Key:** `SECRET_KEY`
- **Value:** `sua-chave-secreta-muito-segura-aqui` (gere uma aleatória)

Para gerar uma chave secreta segura, você pode usar:
```python
import secrets
print(secrets.token_hex(32))
```

### 5️⃣ Fazer o Deploy

1. Revise todas as configurações
2. Clique em **"Create Web Service"**
3. Aguarde o processo de deploy (leva ~2-5 minutos):
   - O Render irá:
     - Clonar seu repositório
     - Instalar as dependências
     - Iniciar a aplicação com Gunicorn
   
4. Monitore os logs na página do dashboard

### 6️⃣ Acessar sua Aplicação

Após o deploy bem-sucedido:

1. A URL será algo como: `https://sistema-produtos.onrender.com`
2. Clique no link para abrir sua aplicação
3. ✅ Pronto! Sua aplicação está no ar!

## 📊 Status do Deploy

O Render mostrará um dos seguintes status:

- 🔵 **Building**: Instalando dependências
- 🟢 **Live**: Aplicação funcionando
- 🔴 **Build Failed**: Erro no deploy (verifique os logs)
- ⚪ **Sleeping**: Plano Free em modo inativo

## 🔧 Troubleshooting

### Problema: Build Failed

**Solução:**
1. Verifique os logs no Render Dashboard
2. Confirme que `requirements.txt` está correto
3. Verifique se `Procfile` contém: `web: gunicorn app:app`
4. Certifique-se que `runtime.txt` especifica uma versão Python válida

### Problema: Application Error

**Solução:**
1. Verifique os logs de runtime
2. Confirme que todas as dependências estão em `requirements.txt`
3. Teste localmente com: `gunicorn app:app`

### Problema: Dados são perdidos após redeploy

**Explicação:**
- O plano Free usa armazenamento efêmero
- Arquivos são perdidos em cada deploy

**Soluções:**
1. **Opção 1:** Upgrade para plano pago (armazenamento persistente)
2. **Opção 2:** Usar banco de dados PostgreSQL (Render oferece PostgreSQL gratuito)
3. **Opção 3:** Usar serviço externo de armazenamento (AWS S3, etc.)

## 🔄 Atualizações e Redesploys

Sempre que você fizer push para o GitHub:

```bash
git add .
git commit -m "Descrição das mudanças"
git push origin main
```

O Render automaticamente:
1. Detecta as mudanças
2. Faz um novo deploy
3. Atualiza a aplicação

## 📱 Monitoramento

No Dashboard do Render, você pode:

- ✅ Ver logs em tempo real
- ✅ Monitorar uso de recursos
- ✅ Configurar alertas
- ✅ Ver métricas de uptime

## 💡 Dicas para Produção

1. **Adicione PostgreSQL para persistência:**
   - No Render, crie um PostgreSQL Database
   - Conecte ao seu Web Service
   - Modifique o código para usar PostgreSQL ao invés de JSON

2. **Configure um domínio customizado:**
   - Em Settings > Custom Domain
   - Adicione seu próprio domínio

3. **Habilite HTTPS:**
   - Render fornece SSL/TLS gratuito automaticamente

4. **Monitoring:**
   - Configure alertas de downtime
   - Use ferramentas como UptimeRobot para monitoramento externo

## 🎯 Checklist Final

Antes do deploy, confirme:

- ✅ Código funciona localmente
- ✅ `requirements.txt` está atualizado
- ✅ `Procfile` existe e está correto
- ✅ `runtime.txt` especifica versão Python correta
- ✅ `.gitignore` exclui arquivos sensíveis
- ✅ Código está no GitHub
- ✅ SECRET_KEY configurada (produção)

## 📞 Suporte

- **Documentação Render:** https://render.com/docs
- **Comunidade:** https://community.render.com
- **Status:** https://status.render.com

---

🎉 **Parabéns! Sua aplicação está pronta para o mundo!**
