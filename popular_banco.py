from app import create_app, db
from app.models import ConfiguracaoSite, Convidado, Presente, Admin
from datetime import datetime, date

app = create_app()
app.app_context().push()

print("🎯 POPULANDO BANCO DE DADOS COM DADOS DE EXEMPLO")
print("=" * 55)

# Atualizar configuração do site com mais informações
config = ConfiguracaoSite.query.first()
if config:
    config.data_casamento = date(2025, 11, 28)  # 28 de novembro de 2025
    config.horario_cerimonia = datetime.strptime("16:00", "%H:%M").time()
    config.horario_festa = datetime.strptime("18:00", "%H:%M").time()
    config.local_cerimonia = "Igreja São Francisco de Assis"
    config.endereco_cerimonia = "Rua das Flores, 123 - Centro, São Paulo - SP"
    config.local_festa = "Espaço Jardim Encantado"
    config.endereco_festa = "Av. Paulista, 456 - Bela Vista, São Paulo - SP"
    config.mensagem_principal = "Criamos esse site para compartilhar com vocês os detalhes da organização do nosso casamento. ♥"
    
    db.session.commit()
    print("✅ Configuração do site atualizada!")

# Adicionar alguns convidados de exemplo
convidados_exemplo = [
    {"nome": "Maria Silva", "email": "maria@email.com", "telefone": "(11) 99999-1111"},
    {"nome": "João Santos", "email": "joao@email.com", "telefone": "(11) 99999-2222"},
    {"nome": "Ana Costa", "email": "ana@email.com", "telefone": "(11) 99999-3333"},
    {"nome": "Pedro Oliveira", "email": "pedro@email.com", "telefone": "(11) 99999-4444"},
    {"nome": "Carla Lima", "email": "carla@email.com", "telefone": "(11) 99999-5555"},
]

for conv_data in convidados_exemplo:
    # Verificar se o convidado já existe
    convidado_existente = Convidado.query.filter_by(email=conv_data["email"]).first()
    if not convidado_existente:
        convidado = Convidado(
            nome=conv_data["nome"],
            email=conv_data["email"],
            telefone=conv_data["telefone"],
            confirmou_presenca=False
        )
        db.session.add(convidado)

db.session.commit()
print("✅ Convidados de exemplo adicionados!")

# Adicionar lista de presentes
presentes_exemplo = [
    {
        "nome": "Jogo de Panelas Antiaderente",
        "categoria": "Cozinha",
        "descricao": "Conjunto com 5 panelas antiaderentes de alta qualidade",
        "preco_sugerido": 299.90,
        "link_loja": "https://www.exemplo.com/panelas",
        "disponivel": True
    },
    {
        "nome": "Jogo de Cama Casal King",
        "categoria": "Quarto",
        "descricao": "Jogo de cama 100% algodão, 300 fios",
        "preco_sugerido": 189.90,
        "link_loja": "https://www.exemplo.com/jogo-cama",
        "disponivel": True
    },
    {
        "nome": "Cafeteira Elétrica",
        "categoria": "Eletrodomésticos",
        "descricao": "Cafeteira elétrica programável para 12 xícaras",
        "preco_sugerido": 159.90,
        "link_loja": "https://www.exemplo.com/cafeteira",
        "disponivel": True
    },
    {
        "nome": "Conjunto de Taças de Cristal",
        "categoria": "Mesa",
        "descricao": "6 taças de cristal para vinho e champagne",
        "preco_sugerido": 249.90,
        "link_loja": "https://www.exemplo.com/tacas",
        "disponivel": True
    },
    {
        "nome": "Aspirador de Pó Robot",
        "categoria": "Limpeza",
        "descricao": "Aspirador robô inteligente com mapeamento",
        "preco_sugerido": 899.90,
        "link_loja": "https://www.exemplo.com/aspirador",
        "disponivel": True
    },
    {
        "nome": "Kit de Utensílios de Cozinha",
        "categoria": "Cozinha",
        "descricao": "Kit completo com colheres, espátulas e utensílios",
        "preco_sugerido": 89.90,
        "link_loja": "https://www.exemplo.com/utensilios",
        "disponivel": True
    },
    {
        "nome": "Conjunto de Toalhas de Banho",
        "categoria": "Banho",
        "descricao": "4 toalhas de banho 100% algodão felpudo",
        "preco_sugerido": 129.90,
        "link_loja": "https://www.exemplo.com/toalhas",
        "disponivel": True
    },
    {
        "nome": "Liquidificador de Alta Potência",
        "categoria": "Eletrodomésticos",
        "descricao": "Liquidificador 1000W com 12 velocidades",
        "preco_sugerido": 199.90,
        "link_loja": "https://www.exemplo.com/liquidificador",
        "disponivel": True
    },
    {
        "nome": "Aparelho de Jantar",
        "categoria": "Mesa",
        "descricao": "Aparelho de jantar em porcelana para 6 pessoas",
        "preco_sugerido": 349.90,
        "link_loja": "https://www.exemplo.com/aparelho-jantar",
        "disponivel": True
    },
    {
        "nome": "Ferro de Passar a Vapor",
        "categoria": "Eletrodomésticos",
        "descricao": "Ferro de passar com gerador de vapor",
        "preco_sugerido": 179.90,
        "link_loja": "https://www.exemplo.com/ferro",
        "disponivel": True
    }
]

for presente_data in presentes_exemplo:
    # Verificar se o presente já existe
    presente_existente = Presente.query.filter_by(nome=presente_data["nome"]).first()
    if not presente_existente:
        presente = Presente(
            nome=presente_data["nome"],
            categoria=presente_data["categoria"],
            descricao=presente_data["descricao"],
            preco_sugerido=presente_data["preco_sugerido"],
            link_loja=presente_data["link_loja"],
            disponivel=presente_data["disponivel"]
        )
        db.session.add(presente)

db.session.commit()
print("✅ Lista de presentes criada!")

print("\n" + "=" * 55)
print("🎉 BANCO DE DADOS POPULADO COM SUCESSO!")
print("\n📊 RESUMO:")
print(f"👥 Administradores: {Admin.query.count()}")
print(f"💌 Convidados: {Convidado.query.count()}")
print(f"🎁 Presentes: {Presente.query.count()}")
print(f"⚙️  Configurações: {ConfiguracaoSite.query.count()}")
