from app import create_app
from app.models import Convidado, db

app = create_app()

with app.app_context():
    print("🔍 Testando criação de convidado diretamente...")
    
    try:
        # Tentar criar um convidado de teste
        novo_convidado = Convidado(
            nome='Teste Direto',
            telefone='(11) 99999-9999',
            email='teste@direto.com',
            acompanhantes=1,
            observacoes='Teste direto no banco',
            confirmado=True,
            liberado_recepcao=True
        )
        
        db.session.add(novo_convidado)
        db.session.commit()
        
        print("✅ Convidado criado com sucesso!")
        
        # Verificar se foi criado
        convidado = Convidado.query.filter_by(nome='Teste Direto').first()
        if convidado:
            print(f"✅ Convidado encontrado: {convidado.nome}")
            print(f"   ID: {convidado.id}")
            print(f"   Email: {convidado.email}")
            print(f"   Confirmado: {convidado.confirmado}")
            print(f"   Liberado: {convidado.liberado_recepcao}")
        else:
            print("❌ Convidado não encontrado após criação")
            
    except Exception as e:
        print(f"❌ Erro ao criar convidado: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
        
    # Listar todos os convidados
    try:
        todos_convidados = Convidado.query.all()
        print(f"\n📋 Total de convidados no banco: {len(todos_convidados)}")
        for c in todos_convidados:
            print(f"  - {c.nome} ({c.email}) - Confirmado: {c.confirmado}")
    except Exception as e:
        print(f"❌ Erro ao listar convidados: {e}")
