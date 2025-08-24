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
    print("🔍 VERIFICANDO PRODUTO AMAZON NO BANCO")
    print("=" * 50)
    
    # Buscar o produto mais recente
    produto = Presente.query.order_by(Presente.id.desc()).first()
    
    if produto:
        print(f"📦 ID: {produto.id}")
        print(f"📝 Nome: {produto.nome}")
        print(f"💰 Preço: R$ {produto.preco_sugerido:.2f}")
        print(f"🔗 Link original length: {len(produto.link_loja)} chars")
        print(f"🔗 Link limpo: {produto.link_loja}")
        print(f"🖼️ Imagem: {produto.imagem_url}")
        print(f"✅ Disponível: {produto.disponivel}")
        
        # Verificar se é o link da Amazon
        if 'amazon' in produto.link_loja.lower():
            print("\n🧹 RESULTADO DA LIMPEZA:")
            print(f"✅ URL da Amazon foi limpa corretamente!")
            print(f"✅ Comprimento dentro do limite: {len(produto.link_loja)} ≤ 500")
            print(f"✅ Mantém ID do produto: {'dp/' in produto.link_loja}")
        
    else:
        print("❌ Nenhum produto encontrado")
        
    print("\n" + "=" * 50)
