# Deploy para Produção - Convite Iara & Samuel

## 🚀 Configuração para Railway (PostgreSQL)

### 1. Configurar PostgreSQL
A aplicação já está configurada para usar o banco PostgreSQL fornecido:
```
postgresql://postgres:WRCdYiMGmLhZfsBqFelhfOTpRCQsNIEp@tramway.proxy.rlwy.net:19242/railway
```

### 2. Instalar psycopg2 em Produção
Adicione ao requirements.txt se não estiver:
```
psycopg2-binary==2.9.7
```

### 3. Variáveis de Ambiente de Produção
```bash
DATABASE_URL=postgresql://postgres:WRCdYiMGmLhZfsBqFelhfOTpRCQsNIEp@tramway.proxy.rlwy.net:19242/railway
SECRET_KEY=chave_secreta_super_segura_para_producao_2024
FLASK_ENV=production
FLASK_DEBUG=False
```

### 4. Comandos de Deploy
```bash
# 1. Fazer push para GitHub
git add .
git commit -m "Deploy inicial do convite"
git push origin main

# 2. Configurar Railway
railway login
railway link [project-id]
railway up
```

## 🔧 Configuração Heroku (Alternativa)

### 1. Procfile
Criar arquivo `Procfile`:
```
web: gunicorn run:app
```

### 2. Adicionar Gunicorn
Adicionar ao requirements.txt:
```
gunicorn==20.1.0
```

### 3. Deploy
```bash
heroku create convite-iara-samuel
heroku addons:create heroku-postgresql:mini
heroku config:set SECRET_KEY=sua_chave_secreta
git push heroku main
```

## 🐳 Deploy com Docker

### 1. Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
```

### 2. docker-compose.yml
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/convite
      - SECRET_KEY=sua_chave_secreta
    depends_on:
      - db
  
  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=convite
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## ⚡ Otimizações para Produção

### 1. Configurações de Segurança
No arquivo `.env` de produção:
```bash
SECRET_KEY=chave_muito_segura_e_aleatoria
FLASK_ENV=production
FLASK_DEBUG=False
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
```

### 2. Logging
Adicionar ao `run.py`:
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/convite.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Convite Iara & Samuel startup')
```

### 3. Cache Estático
Configurar nginx ou CloudFlare para cache de arquivos CSS/JS.

### 4. Backup do Banco
Configurar backup automático do PostgreSQL:
```bash
# Comando de backup
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d_%H%M%S).sql

# Restaurar backup
psql $DATABASE_URL < backup_file.sql
```

## 📱 Configurações de Domínio

### 1. Domínio Personalizado
- Configurar DNS: `convite.iarasamuel.com.br`
- Certificado SSL automático via Railway/Heroku
- Redirects HTTP → HTTPS

### 2. Subdomínios
- `www.convite.iarasamuel.com.br` → redirect para principal
- `admin.convite.iarasamuel.com.br` → acesso direto ao painel

## 🔍 Monitoramento

### 1. Logs de Acesso
- Monitorar acessos aos convites individuais
- Tracking de confirmações de presença
- Alertas para problemas de acesso

### 2. Métricas
- Número de visitantes únicos
- Taxa de confirmação de presença
- Presentes mais escolhidos

### 3. Alertas
- Email para novas confirmações
- Notificação de novos presentes escolhidos
- Alertas de erro no sistema

## 🔒 Segurança em Produção

### 1. HTTPS Obrigatório
```python
@app.before_request
def force_https():
    if not request.is_secure and app.env != 'development':
        return redirect(request.url.replace('http://', 'https://'))
```

### 2. Rate Limiting
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

### 3. Validação Extra
- Validar tokens de convidados
- Sanitizar inputs do usuário
- Logs de tentativas de acesso inválido

## 📊 Backup e Recuperação

### 1. Backup Automático
Configurar backup diário do banco PostgreSQL no Railway:
```bash
# Via Railway CLI
railway db backup create
railway db backup list
railway db backup restore [backup-id]
```

### 2. Backup de Arquivos
- Imagens de presentes
- Logs da aplicação
- Configurações personalizadas

### 3. Plano de Recuperação
- Tempo máximo de downtime: 2 horas
- Backup de redundância em 3 locais
- Procedimentos documentados

## 🎯 Checklist de Deploy

- [ ] Configurar variáveis de ambiente
- [ ] Testar conexão com PostgreSQL
- [ ] Configurar domínio e SSL
- [ ] Implementar logs de produção
- [ ] Configurar backups automáticos
- [ ] Testar todas as funcionalidades
- [ ] Configurar monitoramento
- [ ] Documentar procedimentos
- [ ] Treinar usuários administradores
- [ ] Plano de contingência

---

**🎉 Sucesso no deploy! Que o casamento seja maravilhoso! 💕**
