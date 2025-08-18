# 💕 Sistema de Convite de Casamento - Iara & Samuel

Um sistema completo de convite de casamento interativo, inspirado no design romântico do site noivos.casar.com, desenvolvido com Python/Flask, HTML/CSS/JavaScript e PostgreSQL.

## ✨ Funcionalidades

### 🎯 Para os Convidados
- **Página Principal**: Design romântico com countdown para o casamento
- **Confirmação de Presença**: Formulário completo com dados dos acompanhantes
- **Lista de Presentes**: Catálogo interativo com filtros por categoria
- **Escolha de Presentes**: Sistema de reserva de presentes com formulário
- **Informações do Evento**: Detalhes da cerimônia e festa com integração ao Google Maps
- **Design Responsivo**: Otimizado para celular, tablet e desktop

### 👑 Para os Noivos (Painel Admin)
- **Dashboard Completo**: Estatísticas em tempo real de confirmações e presentes
- **Gerenciamento de Convidados**: Visualização e controle de todas as confirmações
- **Gerenciamento de Presentes**: Adicionar, editar e organizar lista de presentes
- **Configurações**: Editar informações do casal, evento e mensagens
- **Mensagens**: Visualizar mensagens carinhosas dos convidados
- **Relatórios**: Gráficos e estatísticas detalhadas

## 🎨 Design

O projeto utiliza uma paleta de cores romântica inspirada no modelo de referência:
- **Dourado Suave** (#d4a574) - Cor principal
- **Rosa Claro** (#f4e4d6) - Cor secundária  
- **Dourado Escuro** (#c9a876) - Cor de destaque
- **Background Cremoso** (#fefcf9) - Fundo principal

## 🚀 Tecnologias Utilizadas

- **Backend**: Python 3.8+ com Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Banco de Dados**: PostgreSQL (Railway) / SQLite (desenvolvimento)
- **Autenticação**: Flask-Login
- **Formulários**: Flask-WTF
- **ORM**: SQLAlchemy
- **Estilização**: CSS customizado com variáveis e animações
- **Icons**: Font Awesome 6
- **Fontes**: Google Fonts (Dancing Script, Poppins)

## 📁 Estrutura do Projeto

```
convite_iara_samuel/
├── app/
│   ├── __init__.py              # Configuração principal do Flask
│   ├── extensions.py            # Extensões (SQLAlchemy, Login Manager)
│   ├── models.py               # Modelos do banco de dados
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py             # Rotas principais (público)
│   │   ├── admin.py            # Rotas administrativas
│   │   └── convite.py          # Rotas específicas do convite
│   ├── templates/
│   │   ├── base.html           # Template base
│   │   ├── index.html          # Página principal
│   │   ├── presentes.html      # Lista de presentes
│   │   ├── confirmar_presenca.html  # Confirmação de presença
│   │   └── admin/
│   │       ├── login.html      # Login administrativo
│   │       └── dashboard.html  # Dashboard admin
│   └── static/
│       ├── css/
│       │   └── style.css       # Estilos principais
│       ├── js/
│       │   └── main.js         # JavaScript principal
│       └── img/                # Imagens do projeto
├── instance/                   # Arquivos de instância (SQLite)
├── .env.example               # Exemplo de configuração
├── requirements.txt           # Dependências Python
├── run.py                     # Arquivo principal de execução
└── README.md                  # Este arquivo
```

## 🛠️ Instalação e Configuração

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Conta no Railway (para PostgreSQL em produção)

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/convite-iara-samuel.git
cd convite-iara-samuel
```

### 2. Crie um ambiente virtual
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
```bash
# Copie o arquivo de exemplo
copy .env.example .env

# Edite o arquivo .env com suas configurações
```

### 5. Configure o banco de dados

#### Para desenvolvimento (SQLite)
O projeto já vem configurado para usar SQLite automaticamente em desenvolvimento.

#### Para produção (PostgreSQL/Railway)
1. Crie uma conta no [Railway](https://railway.app/)
2. Crie um novo projeto PostgreSQL
3. Copie a URL de conexão
4. Adicione no arquivo `.env`:
```env
DATABASE_URL=postgresql://usuario:senha@host:porta/database
```

### 6. Execute a aplicação
```bash
python run.py
```

A aplicação estará disponível em: http://localhost:5000

## 🔐 Acesso Administrativo

### Credenciais Padrão
- **Usuário**: admin
- **Senha**: admin

⚠️ **IMPORTANTE**: Altere as credenciais padrão em produção!

### Como alterar credenciais
1. Acesse o painel admin
2. Vá em "Configurações"
3. Altere usuário e senha
4. Ou edite diretamente no banco de dados

## 🗃️ Banco de Dados

### Modelos Principais

#### ConfiguracaoSite
- Informações do casal e evento
- Datas, locais e horários
- Mensagens personalizadas

#### Usuario (Admin)
- Credenciais de acesso ao painel
- Sistema de autenticação

#### Convidado
- Dados dos convidados
- Status de confirmação
- Informações dos acompanhantes
- Restrições alimentares

#### Presente
- Catálogo de presentes
- Categorias e descrições
- Preços e links das lojas
- Status de disponibilidade

#### EscolhaPresente
- Registro de presentes escolhidos
- Dados do presenteador
- Data da escolha
- Mensagens dos presenteadores

## 🎯 Como Usar

### Para os Convidados

1. **Acessar o Site**: Visite a URL do convite
2. **Navegar**: Explore as seções do menu
3. **Confirmar Presença**: 
   - Clique em "Confirmar Presença"
   - Preencha seus dados
   - Informe acompanhantes se houver
   - Selecione eventos que participará
4. **Escolher Presente**:
   - Acesse "Lista de Presentes"
   - Filtre por categoria
   - Clique em "Escolher Este Presente"
   - Preencha seus dados

### Para os Noivos (Admin)

1. **Acessar Admin**: /admin ou link no footer
2. **Fazer Login**: Use as credenciais configuradas
3. **Dashboard**: Visualize estatísticas em tempo real
4. **Gerenciar**:
   - **Convidados**: Veja confirmações e dados
   - **Presentes**: Adicione/edite presentes
   - **Configurações**: Personalize informações
   - **Mensagens**: Leia mensagens dos convidados

## 🎨 Personalização

### Cores e Estilo
Edite o arquivo `app/static/css/style.css`:

```css
:root {
    --primary-color: #d4a574;      /* Dourado suave */
    --secondary-color: #f4e4d6;    /* Rosa claro */
    --accent-color: #c9a876;       /* Dourado escuro */
    /* ... outras variáveis */
}
```

### Informações do Casal
1. Acesse o painel admin
2. Vá em "Configurações"
3. Edite nomes, datas, locais e mensagens

### Adicionar Presentes
1. Painel admin → "Lista de Presentes"
2. Clique em "Adicionar Presente"
3. Preencha informações e salve

### Fotos do Casal
1. Adicione as imagens em `app/static/img/`
2. Nomeie como `noiva.jpg` e `noivo.jpg`
3. Os templates carregarão automaticamente

## 📱 Responsividade

O projeto é totalmente responsivo e foi testado em:
- ✅ Desktop (1920px+)
- ✅ Laptop (1366px - 1919px)
- ✅ Tablet (768px - 1365px)
- ✅ Mobile (320px - 767px)

## 🚀 Deploy

### Railway (Recomendado)

1. **Conectar GitHub**:
   - Faça push do código para o GitHub
   - Conecte o repositório no Railway

2. **Configurar Variáveis**:
   ```env
   SECRET_KEY=sua-chave-secreta-forte
   DATABASE_URL=postgresql://...
   FLASK_ENV=production
   ```

3. **Deploy Automático**:
   - O Railway detectará automaticamente o projeto Python
   - O deploy será feito automaticamente

### Outras Plataformas
- **Heroku**: Use o mesmo processo com Procfile
- **Vercel**: Configure para Python
- **DigitalOcean**: Use App Platform

## 🔧 Troubleshooting

### Problemas Comuns

**Erro de importação**:
```bash
# Verifique se está no ambiente virtual
pip install -r requirements.txt
```

**Banco não conecta**:
```bash
# Verifique a URL no .env
# Teste a conexão PostgreSQL
```

**CSS não carrega**:
```bash
# Verifique se os arquivos estão em static/
# Limpe o cache do navegador
```

### Logs de Debug
```python
# Em run.py, certifique-se que debug=True
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 💌 Suporte

- **Issues**: [GitHub Issues](https://github.com/seu-usuario/convite-iara-samuel/issues)
- **Email**: seu-email@exemplo.com
- **Documentação**: Este README

## 🎉 Agradecimentos

- Design inspirado em: [noivos.casar.com](https://noivos.casar.com/demo-26)
- Icons: [Font Awesome](https://fontawesome.com/)
- Fontes: [Google Fonts](https://fonts.google.com/)
- Framework: [Flask](https://flask.palletsprojects.com/)

---

**Feito com ❤️ para Iara & Samuel**

*Que este site ajude a tornar seu casamento ainda mais especial!* 💕
