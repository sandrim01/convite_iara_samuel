import requests
from bs4 import BeautifulSoup
import sys

def testar_pagina_admin_presentes():
    print("🔍 Testando página admin de presentes...")
    
    # URL base
    base_url = "http://127.0.0.1:5000"
    
    # Sessão para manter cookies
    session = requests.Session()
    
    try:
        # 1. Fazer login no admin
        print("📝 Fazendo login no admin...")
        login_data = {
            'username': 'master',
            'password': 'master123'
        }
        
        login_response = session.post(f"{base_url}/admin/login", data=login_data)
        
        if login_response.status_code != 200:
            print(f"❌ Erro no login: {login_response.status_code}")
            return
            
        print("✅ Login realizado com sucesso!")
        
        # 2. Acessar página de presentes
        print("🎁 Acessando página de presentes...")
        presentes_response = session.get(f"{base_url}/admin/presentes")
        
        if presentes_response.status_code != 200:
            print(f"❌ Erro ao acessar presentes: {presentes_response.status_code}")
            return
            
        print("✅ Página de presentes carregada!")
        
        # 3. Analisar HTML
        soup = BeautifulSoup(presentes_response.text, 'html.parser')
        
        # Verificar se existe CSS inline
        style_tags = soup.find_all('style')
        print(f"📊 CSS inline encontrado: {len(style_tags)} blocos")
        
        # Verificar se existe o hero admin
        hero_admin = soup.find(class_='hero-admin')
        if hero_admin:
            print("✅ Hero admin encontrado")
        else:
            print("❌ Hero admin NÃO encontrado")
            
        # Verificar se existe stats-grid
        stats_grid = soup.find(class_='stats-grid')
        if stats_grid:
            print("✅ Stats grid encontrado")
        else:
            print("❌ Stats grid NÃO encontrado")
            
        # Verificar se existe gifts-grid
        gifts_grid = soup.find(class_='gifts-grid')
        if gifts_grid:
            print("✅ Gifts grid encontrado")
        else:
            print("❌ Gifts grid NÃO encontrado")
            
        # Verificar links CSS
        css_links = soup.find_all('link', rel='stylesheet')
        print(f"🎨 Links CSS encontrados: {len(css_links)}")
        for link in css_links:
            print(f"   - {link.get('href', 'N/A')}")
            
        # Salvar HTML para debug
        with open('debug_admin_presentes.html', 'w', encoding='utf-8') as f:
            f.write(presentes_response.text)
        print("💾 HTML salvo em debug_admin_presentes.html")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Servidor não está rodando em http://127.0.0.1:5000")
        print("   Execute 'python run.py' antes de rodar este teste")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    testar_pagina_admin_presentes()
