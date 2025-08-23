#!/usr/bin/env python3
"""
Teste da nova funcionalidade de adicionar presente por link
"""

import requests
import json

def testar_adicionar_por_link():
    try:
        # Primeiro, fazer login
        session = requests.Session()
        
        # Acessar página de login
        login_url = "http://127.0.0.1:5000/admin/login"
        response = session.get(login_url)
        print(f"Status login page: {response.status_code}")
        
        # Fazer login
        login_data = {
            'username': 'master',
            'password': 'master123'
        }
        
        response = session.post(login_url, data=login_data, allow_redirects=True)
        print(f"Status após login: {response.status_code}")
        
        # Testar adicionar presente por link
        link_teste = "https://www.amazon.com.br/dp/B08N5WRWNW"  # Link de exemplo
        
        adicionar_url = "http://127.0.0.1:5000/admin/adicionar-presente-por-link"
        dados = {
            'link': link_teste
        }
        
        response = session.post(
            adicionar_url, 
            json=dados,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status adição por link: {response.status_code}")
        
        if response.status_code == 200:
            resultado = response.json()
            if resultado.get('success'):
                print("✅ Presente adicionado com sucesso!")
                print(f"Mensagem: {resultado.get('message')}")
            else:
                print(f"❌ Erro: {resultado.get('error')}")
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            print(f"Resposta: {response.text[:500]}")
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")

if __name__ == "__main__":
    print("🧪 Testando adição de presente por link...")
    testar_adicionar_por_link()
