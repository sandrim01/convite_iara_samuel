#!/usr/bin/env python3

"""
Teste simplificado de extração de informações de produto
"""

import requests
from bs4 import BeautifulSoup
import re

def extrair_nome_simples(soup):
    """Extrai o nome do produto de forma simplificada"""
    # Tentar extrair de meta tags primeiro (mais confiável)
    meta_title = soup.find('meta', property='og:title')
    if meta_title:
        nome = meta_title.get('content', '').strip()
        if nome:
            return nome
    
    # Tentar h1 tags
    h1_tags = soup.find_all('h1')
    for h1 in h1_tags:
        texto = h1.get_text().strip()
        if texto and len(texto) > 5:  # Nome deve ter pelo menos 5 caracteres
            return texto
    
    # Fallback para título da página
    title = soup.find('title')
    if title:
        titulo = title.get_text().strip()
        # Remover partes comuns do título
        titulo = re.sub(r'\s*[|-]\s*(Amazon|Mercado Livre|Magazine Luiza|Americanas).*$', '', titulo, flags=re.IGNORECASE)
        if titulo:
            return titulo
    
    return 'Produto'

def extrair_preco_simples(soup):
    """Extrai o preço do produto de forma simplificada"""
    # Procurar por textos que contenham preços
    texto_completo = soup.get_text()
    
    # Padrões de preço em Real
    padroes = [
        r'R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)',  # R$ 123.456,89
        r'(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)\s*reais?',  # 123.456,89 reais
    ]
    
    for padrao in padroes:
        matches = re.findall(padrao, texto_completo, re.IGNORECASE)
        if matches:
            # Pegar o primeiro preço encontrado que seja maior que 1
            for match in matches:
                valor_num = float(match.replace('.', '').replace(',', '.'))
                if valor_num > 1:  # Preço maior que R$ 1,00
                    return f"R$ {match}"
    
    return 'R$ 0,00'

def extrair_imagem_simples(soup, link_original):
    """Extrai a URL da imagem do produto"""
    # Tentar meta tag og:image primeiro
    meta_img = soup.find('meta', property='og:image')
    if meta_img:
        img_url = meta_img.get('content', '').strip()
        if img_url:
            # Converter URL relativa para absoluta se necessário
            if img_url.startswith('//'):
                img_url = 'https:' + img_url
            elif img_url.startswith('/'):
                from urllib.parse import urljoin
                img_url = urljoin(link_original, img_url)
            return img_url
    
    # Procurar primeira imagem de produto
    img_tags = soup.find_all('img')
    for img in img_tags:
        src = img.get('src', '') or img.get('data-src', '')
        alt = img.get('alt', '').lower()
        
        # Filtrar imagens que pareçam ser de produtos
        if src and any(palavra in alt for palavra in ['product', 'produto', 'item']):
            if src.startswith('//'):
                src = 'https:' + src
            elif src.startswith('/'):
                from urllib.parse import urljoin
                src = urljoin(link_original, src)
            return src
    
    return ''

def testar_extracao_link(link):
    """Testa a extração de informações de um link"""
    try:
        print(f"🌐 Testando extração do link: {link}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        response = requests.get(link, headers=headers, timeout=15)
        response.raise_for_status()
        print(f"✅ Resposta recebida: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        nome = extrair_nome_simples(soup)
        preco = extrair_preco_simples(soup)
        imagem = extrair_imagem_simples(soup, link)
        
        print(f"\n📦 RESULTADOS:")
        print(f"Nome: {nome}")
        print(f"Preço: {preco}")
        print(f"Imagem: {imagem}")
        
        if nome and nome != 'Produto':
            print(f"\n✅ Extração bem-sucedida!")
            return {
                'nome': nome,
                'preco': preco,
                'imagem': imagem
            }
        else:
            print(f"\n❌ Não foi possível extrair informações suficientes")
            return None
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

def testar_site_simples():
    """Testa com um site mais simples primeiro"""
    html_teste = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Liquidificador Philips Walita | Loja Teste</title>
        <meta property="og:title" content="Liquidificador Philips Walita 3 Velocidades 750W">
        <meta property="og:image" content="https://exemplo.com/imagem-liquidificador.jpg">
    </head>
    <body>
        <h1>Liquidificador Philips Walita 3 Velocidades</h1>
        <p>Preço: R$ 299,90</p>
        <img src="/produto.jpg" alt="Liquidificador produto">
    </body>
    </html>
    """
    
    print("🧪 Testando com HTML simulado...")
    soup = BeautifulSoup(html_teste, 'html.parser')
    
    nome = extrair_nome_simples(soup)
    preco = extrair_preco_simples(soup)
    imagem = extrair_imagem_simples(soup, "https://exemplo.com")
    
    print(f"Nome extraído: {nome}")
    print(f"Preço extraído: {preco}")
    print(f"Imagem extraída: {imagem}")
    
    return nome != 'Produto'

if __name__ == "__main__":
    print("🔍 INICIANDO TESTE DE EXTRAÇÃO\n")
    
    # Primeiro teste com HTML simulado
    if testar_site_simples():
        print("✅ Teste básico funcionando!\n")
    else:
        print("❌ Teste básico falhou!\n")
        exit(1)
    
    # Links para testar (sites que normalmente são mais permissivos)
    links_teste = [
        "https://www.magazineluiza.com.br/liquidificador-philips-walita-daily-ri2110-91-550w-com-2-velocidades-copo-1-25l-preto/p/231424700/ed/edlq/",
        "https://www.casasbahia.com.br/liquidificador-mondial-turbo-inox-l-25-li-inox-3-velocidades-600w-copo-cristal-1-25l-55003652/p/55003652",
    ]
    
    for i, link in enumerate(links_teste):
        print(f"🌐 Teste {i+1}: {link}")
        resultado = testar_extracao_link(link)
        
        if resultado:
            print(f"✅ SUCESSO no teste {i+1}!")
            break
        else:
            print(f"❌ Falhou no teste {i+1}")
        print("-" * 50)
    
    print(f"\n🏁 TESTES CONCLUÍDOS!")
