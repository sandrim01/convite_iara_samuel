#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# Adicionar o diretório raiz ao path do Python
sys.path.insert(0, os.path.abspath('.'))

from app import create_app
from app.models import db, Presente

app = create_app()

with app.app_context():
    print("🔍 VERIFICANDO IMAGENS DOS PRODUTOS")
    print("=" * 60)
    
    # Buscar os últimos produtos adicionados
    produtos = Presente.query.order_by(Presente.id.desc()).limit(5).all()
    
    for produto in produtos:
        print(f"\n📦 ID: {produto.id}")
        print(f"📝 Nome: {produto.nome}")
        print(f"🔗 Link: {produto.link_loja}")
        print(f"🖼️ Imagem URL: '{produto.imagem_url}'")
        print(f"📏 Length imagem: {len(produto.imagem_url or '')} chars")
        
        if produto.imagem_url:
            print(f"✅ Tem imagem definida")
            # Testar se a URL da imagem responde
            try:
                import requests
                response = requests.head(produto.imagem_url, timeout=10)
                print(f"🌐 Status da imagem: {response.status_code}")
                if response.status_code == 200:
                    print(f"✅ Imagem acessível")
                else:
                    print(f"❌ Imagem não acessível")
            except Exception as e:
                print(f"❌ Erro ao verificar imagem: {e}")
        else:
            print(f"❌ Sem imagem definida")
        
        print("-" * 40)
        
    print("\n" + "=" * 60)
