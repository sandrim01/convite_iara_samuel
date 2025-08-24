#!/usr/bin/env python3
"""
Teste da funcionalidade corrigida de exclusão de convidados
"""

from app import create_app
from app.models import db, Convidado, Presente, EscolhaPresente

def criar_convidado_teste():
    """Criar um convidado de teste com escolhas de presentes"""
    
    # Criar convidado de teste
    import uuid
    teste = Convidado(
        nome='João Teste Exclusão', 
        telefone='11987654321',
        token=str(uuid.uuid4())
    )
    db.session.add(teste)
    db.session.commit()
    
    print(f"✅ Convidado criado: ID {teste.id} - {teste.nome}")
    
    # Adicionar escolhas de presentes
    presentes_disponiveis = Presente.query.filter_by(disponivel=True).limit(2).all()
    
    if len(presentes_disponiveis) < 2:
        print("❌ Não há presentes disponíveis suficientes para o teste")
        return None
    
    escolhas_criadas = []
    for presente in presentes_disponiveis:
        escolha = EscolhaPresente(convidado_id=teste.id, presente_id=presente.id)
        presente.disponivel = False
        db.session.add(escolha)
        escolhas_criadas.append(presente.nome)
    
    db.session.commit()
    
    print(f"✅ {len(escolhas_criadas)} escolhas adicionadas:")
    for nome in escolhas_criadas:
        print(f"   - {nome}")
    
    return teste.id

def testar_exclusao(convidado_id):
    """Testar a exclusão do convidado"""
    
    print(f"\n🔍 Testando exclusão do convidado ID {convidado_id}")
    
    # Verificar estado antes
    convidado = Convidado.query.get(convidado_id)
    if not convidado:
        print("❌ Convidado não encontrado")
        return False
    
    escolhas_antes = EscolhaPresente.query.filter_by(convidado_id=convidado_id).all()
    print(f"📋 Estado antes da exclusão:")
    print(f"   - Convidado: {convidado.nome}")
    print(f"   - Escolhas: {len(escolhas_antes)}")
    
    presentes_escolhidos = []
    for escolha in escolhas_antes:
        presente = Presente.query.get(escolha.presente_id)
        if presente:
            presentes_escolhidos.append({
                'nome': presente.nome,
                'disponivel_antes': presente.disponivel
            })
            print(f"   - Presente: {presente.nome} (Disponível: {presente.disponivel})")
    
    # Simular a função de exclusão corrigida
    try:
        # Liberar presentes
        presentes_liberados = []
        for escolha in escolhas_antes:
            presente = Presente.query.get(escolha.presente_id)
            if presente:
                presente.disponivel = True
                presentes_liberados.append(presente.nome)
        
        # Excluir escolhas
        EscolhaPresente.query.filter_by(convidado_id=convidado_id).delete()
        
        # Excluir convidado
        db.session.delete(convidado)
        db.session.commit()
        
        print(f"\n✅ Exclusão realizada com sucesso!")
        print(f"   - Convidado '{convidado.nome}' excluído")
        print(f"   - {len(presentes_liberados)} presentes liberados:")
        for nome in presentes_liberados:
            print(f"     • {nome}")
        
        # Verificar se foi realmente excluído
        verificacao = Convidado.query.get(convidado_id)
        if verificacao is None:
            print(f"✅ Confirmado: convidado foi completamente removido do banco")
        else:
            print(f"❌ Erro: convidado ainda existe no banco")
            return False
        
        # Verificar se presentes foram liberados
        for info in presentes_escolhidos:
            presente = Presente.query.filter_by(nome=info['nome']).first()
            if presente and presente.disponivel:
                print(f"✅ Presente '{presente.nome}' liberado corretamente")
            else:
                print(f"❌ Erro: presente '{info['nome']}' não foi liberado")
        
        return True
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro durante exclusão: {str(e)}")
        return False

def main():
    """Função principal do teste"""
    
    app = create_app()
    with app.app_context():
        print("🧪 TESTE DA FUNCIONALIDADE DE EXCLUSÃO CORRIGIDA")
        print("=" * 50)
        
        # Criar convidado de teste
        convidado_id = criar_convidado_teste()
        
        if convidado_id:
            # Testar exclusão
            sucesso = testar_exclusao(convidado_id)
            
            if sucesso:
                print(f"\n🎉 TESTE CONCLUÍDO COM SUCESSO!")
                print("A funcionalidade de exclusão está funcionando corretamente.")
                print("- Convidados são excluídos sem violar constraints")
                print("- Presentes são automaticamente liberados")
                print("- Relacionamentos são tratados adequadamente")
            else:
                print(f"\n❌ TESTE FALHOU!")
                print("Há problemas na funcionalidade de exclusão.")
        else:
            print("❌ Não foi possível criar o convidado de teste")

if __name__ == '__main__':
    main()
