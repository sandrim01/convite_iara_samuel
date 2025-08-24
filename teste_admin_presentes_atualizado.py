#!/usr/bin/env python3
"""
Teste da página de gerenciamento de presentes com estatísticas e nomes dos convidados
"""

from app import create_app
from app.models import db, Convidado, Presente, EscolhaPresente
import uuid

def testar_presentes_admin():
    """Testar a funcionalidade de presentes no admin"""
    
    app = create_app()
    with app.app_context():
        print("🎁 TESTE DA PÁGINA ADMIN DE PRESENTES")
        print("=" * 50)
        
        # Verificar estatísticas
        total_presentes = Presente.query.count()
        total_escolhas = EscolhaPresente.query.count()
        total_disponiveis = total_presentes - total_escolhas
        
        print(f"📊 ESTATÍSTICAS ATUAIS:")
        print(f"   • Total de presentes: {total_presentes}")
        print(f"   • Presentes escolhidos: {total_escolhas}")
        print(f"   • Presentes disponíveis: {total_disponiveis}")
        
        print(f"\n📋 LISTA DE PRESENTES COM CONVIDADOS:")
        
        # Buscar presentes com informações das escolhas
        presentes = Presente.query.order_by(Presente.id).limit(10).all()
        
        for presente in presentes:
            escolha = EscolhaPresente.query.filter_by(presente_id=presente.id).first()
            
            if escolha:
                convidado = Convidado.query.get(escolha.convidado_id)
                if convidado:
                    primeiro_nome = convidado.nome.split()[0] if convidado.nome else 'N/A'
                    status = f"✅ Escolhido por: {primeiro_nome}"
                else:
                    status = "❓ Escolhido (convidado não encontrado)"
            else:
                status = "⭕ Disponível"
            
            preco = f"R$ {presente.preco_sugerido:.2f}" if presente.preco_sugerido else "R$ 0,00"
            print(f"   {presente.id:2d}. {presente.nome[:40]:<40} {preco:>10} - {status}")
        
        # Testar criação de convidado e escolha para verificar
        print(f"\n🧪 TESTE DE NOVA ESCOLHA:")
        
        # Criar convidado de teste
        convidado_teste = Convidado(
            nome='Maria Teste Presentes',
            telefone='11999887766', 
            token=str(uuid.uuid4())
        )
        db.session.add(convidado_teste)
        db.session.commit()
        
        print(f"   ✅ Convidado criado: {convidado_teste.nome} (ID: {convidado_teste.id})")
        
        # Encontrar um presente disponível
        presente_disponivel = None
        for presente in presentes:
            escolha_existente = EscolhaPresente.query.filter_by(presente_id=presente.id).first()
            if not escolha_existente:
                presente_disponivel = presente
                break
        
        if presente_disponivel:
            # Criar uma escolha
            nova_escolha = EscolhaPresente(
                convidado_id=convidado_teste.id,
                presente_id=presente_disponivel.id
            )
            presente_disponivel.disponivel = False
            
            db.session.add(nova_escolha)
            db.session.commit()
            
            print(f"   ✅ Escolha criada: {presente_disponivel.nome} escolhido por Maria")
            
            # Verificar estatísticas atualizadas
            total_presentes_novo = Presente.query.count()
            total_escolhas_novo = EscolhaPresente.query.count()
            total_disponiveis_novo = total_presentes_novo - total_escolhas_novo
            
            print(f"\n📊 ESTATÍSTICAS ATUALIZADAS:")
            print(f"   • Total de presentes: {total_presentes_novo}")
            print(f"   • Presentes escolhidos: {total_escolhas_novo} (+{total_escolhas_novo - total_escolhas})")
            print(f"   • Presentes disponíveis: {total_disponiveis_novo} ({total_disponiveis_novo - total_disponiveis:+d})")
            
            # Limpar teste
            db.session.delete(nova_escolha)
            db.session.delete(convidado_teste)
            presente_disponivel.disponivel = True
            db.session.commit()
            
            print(f"   🧹 Teste limpo - dados removidos")
            
        else:
            # Limpar convidado de teste
            db.session.delete(convidado_teste)
            db.session.commit()
            print(f"   ❌ Nenhum presente disponível para teste")
        
        print(f"\n🎉 TESTE CONCLUÍDO!")
        print("A página de presentes deve exibir:")
        print("  • Estatísticas corretas baseadas na tabela escolha_presente")
        print("  • Nome do primeiro convidado nos presentes escolhidos")
        print("  • Visual atualizado com informação 'Por: Nome'")

if __name__ == '__main__':
    testar_presentes_admin()
