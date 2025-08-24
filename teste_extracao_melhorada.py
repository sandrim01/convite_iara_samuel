#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# Adicionar o diretório raiz ao path do Python
sys.path.insert(0, os.path.abspath('.'))

from app.routes.admin import extrair_informacoes_produto

def testar_extracao_melhorada():
    """Testa a função melhorada de extração"""
    
    link = "https://www.amazon.com.br/C%C3%B4moda-Dit%C3%A1lia-Gavetas-Dm-243-Verde/dp/B0DD5G8CD5/ref=sr_1_1_sspa"
    
    print("🧪 TESTE DA FUNÇÃO MELHORADA")
    print("=" * 60)
    print(f"🔗 URL: {link}")
    
    info = extrair_informacoes_produto(link)
    
    if info:
        print(f"\n✅ INFORMAÇÕES EXTRAÍDAS:")
        print(f"📝 Nome: {info.get('nome', 'N/A')}")
        print(f"💰 Preço: {info.get('preco', 'N/A')}")
        print(f"🖼️ Imagem: {info.get('imagem', 'N/A')}")
        
        if info.get('imagem'):
            print(f"\n✅ IMAGEM ENCONTRADA!")
            print(f"📏 Tamanho da URL: {len(info['imagem'])} chars")
            
            # Testar se a imagem responde
            try:
                import requests
                response = requests.head(info['imagem'], timeout=10)
                print(f"🌐 Status HTTP: {response.status_code}")
                if response.status_code == 200:
                    print(f"✅ Imagem acessível!")
                else:
                    print(f"❌ Imagem não acessível")
            except Exception as e:
                print(f"❌ Erro ao verificar imagem: {e}")
        else:
            print(f"\n❌ IMAGEM NÃO ENCONTRADA")
    else:
        print(f"\n❌ FALHA NA EXTRAÇÃO")

if __name__ == "__main__":
    testar_extracao_melhorada()
