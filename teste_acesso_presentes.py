#!/usr/bin/env python3

"""
Teste de acesso à página de gerenciamento de presentes
"""

import requests
import sys
from urllib.parse import urljoin

def testar_acesso_presentes():
    """Testa o acesso à página de presentes do admin"""
    base_url = "http://127.0.0.1:5000"
    
    # Criar sessão
    session = requests.Session()
    
    try:
        print("🔍 Testando acesso à página de presentes...")
        
        # 1. Tentar acessar página de login
        print("\n1️⃣ Acessando página de login...")
        login_url = f"{base_url}/admin/login"
        response = session.get(login_url)
        print(f"Status login: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ Erro ao acessar login: {response.status_code}")
            return False
        
        # 2. Fazer login
        print("\n2️⃣ Fazendo login...")
        login_data = {
            'username': 'admin',
            'password': 'admin123'
        }
        
        response = session.post(login_url, data=login_data)
        print(f"Status após login: {response.status_code}")
        
        if response.status_code not in [200, 302]:
            print(f"❌ Erro no login: {response.status_code}")
            return False
        
        # 3. Acessar página de presentes
        print("\n3️⃣ Acessando página de presentes...")
        presentes_url = f"{base_url}/admin/presentes"
        response = session.get(presentes_url)
        print(f"Status presentes: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Página de presentes acessível!")
            
            # Verificar se o conteúdo básico está presente
            content = response.text
            if "Gerenciar Presentes" in content or "presentes" in content.lower():
                print("✅ Conteúdo da página parece correto!")
                return True
            else:
                print("⚠️ Página carregou mas conteúdo pode estar incorreto")
                # Mostrar parte do conteúdo para debug
                print(f"Primeiros 300 caracteres: {content[:300]}")
                return False
        else:
            print(f"❌ Erro ao acessar presentes: {response.status_code}")
            print(f"URL tentada: {presentes_url}")
            
            # Se for 404, tentar dashboard primeiro
            if response.status_code == 404:
                print("\n🔄 Tentando acessar dashboard primeiro...")
                dashboard_url = f"{base_url}/admin/dashboard"
                resp = session.get(dashboard_url)
                print(f"Status dashboard: {resp.status_code}")
                
                if resp.status_code == 200:
                    print("✅ Dashboard acessível, tentando presentes novamente...")
                    resp2 = session.get(presentes_url)
                    print(f"Status presentes (2ª tentativa): {resp2.status_code}")
                    if resp2.status_code == 200:
                        return True
            
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão! O servidor Flask está rodando?")
        print("Execute: python run.py")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

if __name__ == "__main__":
    print("🧪 TESTE DE ACESSO À PÁGINA DE PRESENTES\n")
    
    sucesso = testar_acesso_presentes()
    
    if sucesso:
        print(f"\n🎉 TESTE CONCLUÍDO COM SUCESSO!")
        print("A página de presentes está acessível.")
    else:
        print(f"\n💥 TESTE FALHOU!")
        print("Há algum problema com o acesso à página de presentes.")
        sys.exit(1)
