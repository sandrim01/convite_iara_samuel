#!/usr/bin/env python3
"""
Script para testar especificamente o login e acesso à página de presentes admin
"""

import requests
from bs4 import BeautifulSoup

def teste_login_detalhado():
    """Testa o login de forma mais detalhada"""
    
    session = requests.Session()
    base_url = 'http://127.0.0.1:5000'
    
    print("🔧 TESTE DETALHADO - LOGIN E PRESENTES ADMIN")
    print("=" * 55)
    
    # 1. Acessar página de login
    print("🌐 Acessando página de login...")
    login_page = session.get(f'{base_url}/admin/login')
    print(f"📄 Login page status: {login_page.status_code}")
    
    # 2. Fazer login
    print("🔑 Fazendo login...")
    login_data = {'username': 'master', 'password': 'master123'}
    login_response = session.post(f'{base_url}/admin/login', data=login_data, allow_redirects=False)
    print(f"🔑 Login Status: {login_response.status_code}")
    print(f"🔄 Headers: {dict(login_response.headers)}")
    
    if 'Location' in login_response.headers:
        print(f"📍 Redirecionamento para: {login_response.headers['Location']}")
    
    # 3. Verificar se há cookies de sessão
    print(f"🍪 Cookies: {session.cookies}")
    
    # 4. Seguir redirecionamento se houver
    if login_response.status_code in [301, 302]:
        dashboard_response = session.get(f'{base_url}/admin/')
        print(f"📊 Dashboard Status: {dashboard_response.status_code}")
    
    # 5. Acessar página de presentes
    print("📦 Acessando página de presentes...")
    presentes_response = session.get(f'{base_url}/admin/presentes')
    print(f"📦 Presentes Status: {presentes_response.status_code}")
    
    if presentes_response.status_code != 200:
        print("❌ Erro ao acessar presentes. Vamos ver o conteúdo:")
        print("Conteúdo da resposta:")
        print(presentes_response.text[:1000])
        return
    
    # 6. Analisar conteúdo da página
    soup = BeautifulSoup(presentes_response.text, 'html.parser')
    
    # Verificar se é a página correta
    title = soup.find('title')
    print(f"📰 Título da página: {title.text if title else 'Não encontrado'}")
    
    # Verificar se há o cabeçalho da página de presentes
    h1 = soup.find('h1')
    print(f"🏷️  H1: {h1.text if h1 else 'Não encontrado'}")
    
    # Procurar por presentes
    presente_cards = soup.find_all('div', class_='presente-card')
    print(f"🎁 Cartões de presente encontrados: {len(presente_cards)}")
    
    # Verificar se há um grid vazio ou mensagem
    empty_state = soup.find('div', class_='empty-state') or soup.find('p', string=lambda text: text and 'Nenhum presente' in text)
    if empty_state:
        print(f"📭 Estado vazio encontrado: {empty_state.text}")
    
    # Procurar botão de adicionar
    btn_adicionar = soup.find('a', string=lambda text: text and 'Adicionar' in text) or soup.find('button', string=lambda text: text and 'Adicionar' in text)
    if btn_adicionar:
        print(f"➕ Botão adicionar encontrado: {btn_adicionar.text.strip()}")
    
    # Verificar paginação
    pagination = soup.find('div', class_='pagination')
    if pagination:
        print("📄 Paginação encontrada")
    else:
        print("📄 Paginação não encontrada")
    
    # Procurar informações sobre quantos presentes existem
    stats = soup.find_all('div', class_='stat-card')
    print(f"📊 Cards de estatística encontrados: {len(stats)}")
    for i, stat in enumerate(stats):
        number = stat.find('span', class_='stat-number')
        label = stat.find('div', class_='stat-label')
        if number and label:
            print(f"   {i+1}. {label.text}: {number.text}")
    
    # Salvar para análise
    with open('debug_presentes_admin.html', 'w', encoding='utf-8') as f:
        f.write(presentes_response.text)
    print("📁 HTML da página de presentes salvo em debug_presentes_admin.html")

if __name__ == '__main__':
    teste_login_detalhado()
