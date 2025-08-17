# Convite Interativo - Iara & Samuel 💕

Um sistema completo de convite de casamento interativo desenvolvido em Python/Flask com as seguintes funcionalidades:

## 🎯 Funcionalidades

### ✨ Convite Principal
- **Design romântico e responsivo** - Perfeito para visualização em celulares e computadores
- **Página inicial personalizada** com nomes dos noivos, data e local do casamento
- **Animações e efeitos visuais** incluindo corações flutuantes
- **Lista de presentes pública** para todos os visitantes

### 👥 Sistema de Convidados
- **Links personalizados** - Cada convidado recebe um link único
- **Confirmação de presença** com número de acompanhantes
- **Escolha de presentes** individualizada
- **Sistema de observações** para mensagens especiais

### 🎁 Lista de Presentes
- **Cadastro completo** com nome, descrição, categoria e preço
- **Imagens dos presentes** via URL
- **Links para lojas** onde comprar
- **Controle de disponibilidade** - presentes ficam indisponíveis após escolhidos
- **Gerenciamento de entregas** pelo painel administrativo

### 🔧 Painel Administrativo
- **Dashboard com estatísticas** - Total de convidados, confirmações, presentes
- **Gerenciamento de convidados** - Adicionar, listar, excluir
- **Gerenciamento de presentes** - Adicionar, editar, controlar entregas
- **Configurações do site** - Personalizar cores, textos, datas e locais
- **Geração automática de tokens** únicos para cada convidado

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.8+
- PostgreSQL (para produção) ou SQLite (para desenvolvimento)

### 1. Clone o repositório
\`\`\`bash
git clone https://github.com/sandrim01/convite_iara_samuel.git
cd convite_iara_samuel
\`\`\`

### 2. Instale as dependências
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 3. Configure as variáveis de ambiente
Edite o arquivo \`.env\`:
\`\`\`
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=sua_chave_secreta_super_segura
FLASK_ENV=development
FLASK_DEBUG=True
\`\`\`

### 4. Execute a aplicação
\`\`\`bash
python run.py
\`\`\`

### 5. Configuração inicial
Acesse \`http://localhost:5000/admin/setup\` para criar o primeiro administrador.

## 🎨 Personalização

### Cores e Tema
- Acesse o painel administrativo → Configurações
- Personalize as cores principais do site
- Configure textos personalizados

### Conteúdo
- **Nome dos noivos**: Configurável via painel
- **Data do casamento**: Com formatação automática
- **Locais**: Cerimônia e festa separadamente
- **Mensagens**: Texto principal do convite

## 📱 Como Usar

### Para os Noivos (Administradores)
1. **Primeiro acesso**: Configure o sistema em `/admin/setup`
2. **Adicione convidados**: Cada um receberá um token único
3. **Configure presentes**: Monte sua lista de presentes
4. **Compartilhe links**: Envie para cada convidado seu link personalizado
5. **Acompanhe**: Use o dashboard para ver confirmações e escolhas

### Para os Convidados
1. **Acesse seu link único**: Recebido dos noivos
2. **Confirme presença**: Indique quantos acompanhantes
3. **Escolha presentes**: Selecione da lista disponível
4. **Deixe mensagens**: Campo para observações especiais

## 🔗 Estrutura de URLs

- \`/\` - Página principal do convite
- \`/lista-presentes\` - Lista pública de presentes
- \`/convite/{token}\` - Convite personalizado para cada convidado
- \`/admin/\` - Painel administrativo
- \`/admin/setup\` - Configuração inicial (apenas primeiro acesso)

## 🛡️ Segurança

- **Tokens únicos** para cada convidado (UUID4)
- **Senhas criptografadas** no banco de dados
- **Validação de formulários** tanto no frontend quanto backend
- **Proteção de rotas administrativas** com Flask-Login

## 💾 Banco de Dados

### Tabelas Principais
- **Admin**: Usuários administradores
- **Convidado**: Dados dos convidados e tokens
- **Presente**: Lista de presentes
- **EscolhaPresente**: Relação convidado ↔ presente
- **ConfiguracaoSite**: Configurações gerais

### Desenvolvimento vs Produção
- **Desenvolvimento**: SQLite automático se PostgreSQL não disponível
- **Produção**: PostgreSQL recomendado para melhor performance

## 🎯 Próximas Funcionalidades

- [ ] Upload de imagens para presentes
- [ ] Sistema de notificações por email
- [ ] Exportação de lista de convidados
- [ ] App mobile nativo
- [ ] Integração com redes sociais
- [ ] Sistema de RSVP por WhatsApp

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (\`git checkout -b feature/AmazingFeature\`)
3. Commit suas mudanças (\`git commit -m 'Add some AmazingFeature'\`)
4. Push para a branch (\`git push origin feature/AmazingFeature\`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo \`LICENSE\` para detalhes.

## 💕 Créditos

Desenvolvido com muito amor para Iara & Samuel.

---

**🎉 Que seu casamento seja repleto de amor, alegria e momentos inesquecíveis! 🎉**
