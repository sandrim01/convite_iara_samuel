#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re

def testar_extracao_imagem_amazon():
    """Testa especificamente a extração de imagem da Amazon"""
    
    # URL da Amazon que adicionamos
    link = "https://www.amazon.com.br/C%C3%B4moda-Dit%C3%A1lia-Gavetas-Dm-243-Verde/dp/B0DD5G8CD5/ref=sr_1_1_sspa"
    
    print("🧪 TESTE DE EXTRAÇÃO DE IMAGEM AMAZON")
    print("=" * 60)
    print(f"🔗 URL: {link}")
    
    try:
        # Headers para simular um navegador real
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        print("🌐 Fazendo requisição...")
        response = requests.get(link, headers=headers, timeout=15)
        print(f"✅ Status: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Testar extração og:image
        print("\n1️⃣ Testando meta og:image:")
        meta_img = soup.find('meta', property='og:image')
        if meta_img:
            img_url = meta_img.get('content', '').strip()
            print(f"   ✅ Encontrada: {img_url}")
        else:
            print("   ❌ Não encontrada")
        
        # Testar busca por imagens com alt específico
        print("\n2️⃣ Testando imagens com alt relevante:")
        img_tags = soup.find_all('img')
        print(f"   📊 Total de imagens encontradas: {len(img_tags)}")
        
        for i, img in enumerate(img_tags[:10]):  # Primeiras 10 imagens
            src = img.get('src', '') or img.get('data-src', '')
            alt = img.get('alt', '').lower()
            print(f"   #{i+1}: alt='{alt}' src='{src[:100]}{'...' if len(src) > 100 else ''}'")
            
            if src and any(palavra in alt for palavra in ['product', 'produto', 'item', 'cômoda', 'ditália']):
                print(f"   ⭐ CANDIDATA: {src}")
        
        # Testar busca específica da Amazon
        print("\n3️⃣ Testando seletores específicos da Amazon:")
        selectors = [
            '#landingImage',
            '#imgBlkFront',
            '.a-dynamic-image',
            '.product-image img',
            '[data-a-image-name="landingImage"]'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                src = element.get('src', '') or element.get('data-src', '')
                print(f"   ✅ {selector}: {src}")
            else:
                print(f"   ❌ {selector}: não encontrado")
        
        # Buscar todas as imagens que contenham o ID do produto
        print("\n4️⃣ Testando imagens que contenham ID do produto (B0DD5G8CD5):")
        for i, img in enumerate(img_tags):
            src = img.get('src', '') or img.get('data-src', '')
            if 'B0DD5G8CD5' in src or 'images-amazon' in src:
                print(f"   ⭐ #{i+1}: {src}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    testar_extracao_imagem_amazon()
