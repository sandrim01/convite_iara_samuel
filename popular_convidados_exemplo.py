#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para popular banco com convidados de exemplo
"""

from app import create_app, db
from app.models import Convidado
import uuid
from datetime import datetime

def criar_convidados_exemplo():
    app = create_app()
    
    with app.app_context():
        print("🔄 Criando convidados de exemplo...")
        
        # Verificar se já existem convidados
        existing_count = Convidado.query.count()
        if existing_count > 0:
            print(f"✅ Já existem {existing_count} convidados no banco.")
            return
        
        # Lista de convidados de exemplo
        convidados_exemplo = [
            {
                'nome': 'João Silva',
                'email': 'joao.silva@email.com',
                'telefone': '(11) 99999-1234',
                'confirmacao': True,
                'numero_acompanhantes': 2,
                'liberado_recepcao': True,
                'data_confirmacao': datetime.now(),
                'mensagem': 'Muito feliz em participar deste momento especial!'
            },
            {
                'nome': 'Maria Santos',
                'email': 'maria.santos@email.com',
                'telefone': '(11) 98888-5678',
                'confirmacao': True,
                'numero_acompanhantes': 1,
                'liberado_recepcao': True,
                'data_confirmacao': datetime.now()
            },
            {
                'nome': 'Pedro Oliveira',
                'email': 'pedro.oliveira@email.com',
                'telefone': '(11) 97777-9012',
                'confirmacao': False,
                'numero_acompanhantes': 0,
                'liberado_recepcao': False
            },
            {
                'nome': 'Ana Costa',
                'email': 'ana.costa@email.com',
                'telefone': '(11) 96666-3456',
                'confirmacao': True,
                'numero_acompanhantes': 1,
                'liberado_recepcao': True,
                'data_confirmacao': datetime.now(),
                'mensagem': 'Parabéns pelo casamento! Estaremos lá!'
            },
            {
                'nome': 'Carlos Ferreira',
                'email': 'carlos.ferreira@email.com',
                'telefone': '(11) 95555-7890',
                'confirmacao': False,
                'numero_acompanhantes': 0,
                'liberado_recepcao': False
            },
            {
                'nome': 'Fernanda Lima',
                'email': 'fernanda.lima@email.com',
                'telefone': '(11) 94444-2345',
                'confirmacao': True,
                'numero_acompanhantes': 3,
                'liberado_recepcao': True,
                'data_confirmacao': datetime.now()
            },
            {
                'nome': 'Roberto Alves',
                'email': 'roberto.alves@email.com',
                'telefone': '(11) 93333-6789',
                'confirmacao': False,
                'numero_acompanhantes': 0,
                'liberado_recepcao': False
            },
            {
                'nome': 'Luciana Rocha',
                'email': 'luciana.rocha@email.com',
                'telefone': '(11) 92222-0123',
                'confirmacao': True,
                'numero_acompanhantes': 2,
                'liberado_recepcao': False,
                'data_confirmacao': datetime.now(),
                'mensagem': 'Desejamos muitas felicidades!'
            }
        ]
        
        # Criar os convidados
        for dados in convidados_exemplo:
            # Gerar token único
            token = str(uuid.uuid4())
            
            convidado = Convidado(
                nome=dados['nome'],
                email=dados['email'],
                telefone=dados['telefone'],
                token=token,
                confirmacao=dados['confirmacao'],
                numero_acompanhantes=dados['numero_acompanhantes'],
                liberado_recepcao=dados['liberado_recepcao'],
                data_confirmacao=dados.get('data_confirmacao'),
                mensagem=dados.get('mensagem'),
                created_at=datetime.now()
            )
            
            db.session.add(convidado)
            print(f"✅ Criado: {dados['nome']}")
        
        # Salvar no banco
        db.session.commit()
        
        print(f"\n🎉 {len(convidados_exemplo)} convidados de exemplo criados com sucesso!")
        
        # Mostrar estatísticas
        total = Convidado.query.count()
        confirmados = Convidado.query.filter_by(confirmacao=True).count()
        liberados = Convidado.query.filter_by(liberado_recepcao=True).count()
        
        print(f"\n📊 Estatísticas:")
        print(f"   Total: {total}")
        print(f"   Confirmados: {confirmados}")
        print(f"   Pendentes: {total - confirmados}")
        print(f"   Liberados Recepção: {liberados}")

if __name__ == '__main__':
    criar_convidados_exemplo()
