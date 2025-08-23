#!/usr/bin/env python3
"""
Teste rápido para verificar se a página admin de presentes está funcionando
"""

import requests
import sys

def testar_pagina_presentes():
    try:
        # Primeiro, fazer login
        session = requests.Session()
        
        # Acessar página de login
        login_url = "http://127.0.0.1:5000/admin/login"
        response = session.get(login_url)
        print(f"Status login page: {response.status_code}")
        
        # Fazer login (assumindo que o usuário é master/master123)
        login_data = {
            'username': 'master',
            'password': 'master123'
        }
        
        response = session.post(login_url, data=login_data, allow_redirects=True)
        print(f"Status após login: {response.status_code}")
        print(f"URL final após login: {response.url}")
        
        # Acessar página de presentes
        presentes_url = "http://127.0.0.1:5000/admin/presentes"
        response = session.get(presentes_url)
        print(f"Status página presentes: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Página de presentes está acessível!")
            if "Gerenciar Presentes" in response.text:
                print("✅ Conteúdo da página carregado corretamente!")
            else:
                print("❌ Conteúdo da página pode estar com problemas")
        else:
            print(f"❌ Erro ao acessar página de presentes: {response.status_code}")
            print(f"Conteúdo da resposta: {response.text[:500]}")
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")

if __name__ == "__main__":
    print("🧪 Testando página admin de presentes...")
    testar_pagina_presentes()
