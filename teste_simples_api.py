#!/usr/bin/env python3

"""
Teste simples e direto da API
"""

import requests
import json

def teste_simples():
    """Teste direto da API"""
    # Fazer login primeiro
    session = requests.Session()
    login_response = session.post('http://127.0.0.1:5000/admin/login', data={
        'username': 'admin',
        'password': 'admin123'
    })
    
    print(f"Login status: {login_response.status_code}")
    
    # Testar API
    api_response = session.post(
        'http://127.0.0.1:5000/admin/adicionar-presente-por-link',
        json={'link': 'https://exemplo.com/produto'},
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"API status: {api_response.status_code}")
    print(f"API response: {api_response.text[:500]}")
    
    if api_response.headers.get('content-type', '').startswith('application/json'):
        try:
            data = api_response.json()
            print(f"JSON data: {data}")
        except:
            print("Erro ao decodificar JSON")

if __name__ == "__main__":
    teste_simples()
