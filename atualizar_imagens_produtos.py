#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# Adicionar o diretório raiz ao path do Python
sys.path.insert(0, os.path.abspath('.'))

from app import create_app
from app.models import db, Presente
from app.routes.admin import extrair_informacoes_produto

app = create_app()

with app.app_context():
    print("🔄 ATUALIZANDO IMAGENS DOS PRODUTOS EXISTENTES")
    print("=" * 60)
    
    # Buscar produtos sem imagem
    produtos_sem_imagem = Presente.query.filter(
        (Presente.imagem_url == '') | (Presente.imagem_url.is_(None))
    ).all()
    
    print(f"📊 Produtos sem imagem: {len(produtos_sem_imagem)}")
    
    for produto in produtos_sem_imagem:
        print(f"\n📦 Atualizando produto ID {produto.id}: {produto.nome}")
        print(f"🔗 Link: {produto.link_loja}")
        
        # Extrair informações novamente
        try:
            info = extrair_informacoes_produto(produto.link_loja)
            
            if info and info.get('imagem'):
                produto.imagem_url = info['imagem']
                db.session.commit()
                print(f"✅ Imagem atualizada: {info['imagem']}")
            else:
                print(f"❌ Não foi possível extrair imagem")
                
        except Exception as e:
            print(f"❌ Erro ao atualizar: {e}")
    
    print(f"\n✅ Atualização concluída!")
    print("=" * 60)
