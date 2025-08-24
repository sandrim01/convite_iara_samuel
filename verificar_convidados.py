#!/usr/bin/env python3
"""
Verificar estrutura da tabela convidado e dados
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))
from app import create_app
from app.models import db, Convidado

app = create_app()
with app.app_context():
    # Verificar estrutura da tabela
    from sqlalchemy import text
    result = db.session.execute(text("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'convidado' 
        ORDER BY ordinal_position
    """))
    
    print('📋 Estrutura da tabela Convidado:')
    for row in result:
        print(f'   • {row[0]}: {row[1]}')
    
    print('\n📊 Convidados no banco:')
    for conv in Convidado.query.all():
        print(f'   • ID: {conv.id} - Nome: {conv.nome}')
        telefone_info = conv.telefone if conv.telefone else "Não informado"
        print(f'     Telefone: {telefone_info}')
        print(f'     Liberado: {conv.liberado_recepcao}')
        
        # Verificar se campos WhatsApp existem
        try:
            print(f'     WhatsApp Enviado: {conv.convite_enviado_whatsapp}')
            print(f'     Data Envio: {conv.data_envio_whatsapp}')
        except AttributeError as e:
            print(f'     ❌ ERRO: Campos WhatsApp não existem - {e}')
        print('---')
