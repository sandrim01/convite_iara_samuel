#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import sys
import os

# Adicionar o diretório raiz ao path do Python
sys.path.insert(0, os.path.abspath('.'))

def testar_adicao_novo_produto():
    """Testa a adição de um novo produto com imagem"""
    
    print("🧪 TESTE COMPLETO - ADIÇÃO DE PRODUTO COM IMAGEM")
    print("=" * 60)
    
    # Usar outro produto da Amazon para teste
    link_teste = "https://www.amazon.com.br/Guarda-roupa-Casal-Espelho-Demóbile/dp/B0CJ8KCDM3"
    
    session = requests.Session()
    
    try:
        # 1. Login
        print("🔐 Fazendo login...")
        login_response = session.post('http://127.0.0.1:5000/admin/login', 
                                    data={'username': 'admin', 'password': 'Casamento2025*#'})
        print(f"Status login: {login_response.status_code}")
        
        if login_response.status_code != 200:
            print("❌ Falha no login")
            return
        
        # 2. Adicionar produto
        print(f"🔗 Testando adição do produto: {link_teste}")
        
        add_response = session.post('http://127.0.0.1:5000/admin/adicionar-presente-por-link',
                                  json={'link': link_teste},
                                  headers={'Content-Type': 'application/json'})
        
        print(f"Status da resposta: {add_response.status_code}")
        
        if add_response.status_code == 200:
            data = add_response.json()
            print(f"📋 Resposta: {data}")
            
            if data.get('success'):
                print(f"✅ Produto adicionado com sucesso!")
                print(f"   ID: {data.get('presente_id')}")
                print(f"   Mensagem: {data.get('message')}")
                
                # 3. Verificar se tem imagem
                produto_id = data.get('presente_id')
                if produto_id:
                    verificar_response = session.get(f'http://127.0.0.1:5000/admin/presentes')
                    if verificar_response.status_code == 200:
                        print(f"✅ Página de presentes carregada - verifique se a imagem aparece!")
                    
            else:
                print(f"❌ Erro: {data.get('error')}")
        else:
            print(f"❌ Erro HTTP: {add_response.status_code}")
            print(f"Resposta: {add_response.text}")
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    testar_adicao_novo_produto()
