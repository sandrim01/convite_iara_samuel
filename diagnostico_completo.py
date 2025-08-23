#!/usr/bin/env python3

"""
Diagnóstico detalhado do acesso às páginas do admin
"""

import requests
import sys
from urllib.parse import urljoin

def diagnosticar_acesso():
    """Faz um diagnóstico completo do acesso ao admin"""
    base_url = "http://127.0.0.1:5000"
    
    print("🔍 DIAGNÓSTICO COMPLETO DE ACESSO AO ADMIN\n")
    
    # Teste 1: Servidor está rodando?
    print("1️⃣ Verificando se o servidor está rodando...")
    try:
        response = requests.get(base_url, timeout=5)
        print(f"   ✅ Servidor responde: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ❌ Servidor não está rodando!")
        print("   💡 Execute: python run.py")
        return False
    except Exception as e:
        print(f"   ❌ Erro de conexão: {e}")
        return False
    
    # Teste 2: Página principal do admin
    print("\n2️⃣ Testando página principal do admin...")
    try:
        admin_url = f"{base_url}/admin"
        response = requests.get(admin_url, timeout=5)
        print(f"   Status /admin: {response.status_code}")
        if response.status_code == 302:
            print("   ✅ Redirecionamento normal (302)")
        elif response.status_code == 200:
            print("   ✅ Página carregou (200)")
        else:
            print(f"   ⚠️ Status inesperado: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Teste 3: Página de login
    print("\n3️⃣ Testando página de login...")
    try:
        login_url = f"{base_url}/admin/login"
        response = requests.get(login_url, timeout=5)
        print(f"   Status /admin/login: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Página de login acessível")
            if "login" in response.text.lower() or "entrar" in response.text.lower():
                print("   ✅ Conteúdo da página parece correto")
            else:
                print("   ⚠️ Conteúdo pode estar incorreto")
        else:
            print(f"   ❌ Erro no acesso: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Teste 4: Testar login
    print("\n4️⃣ Testando processo de login...")
    session = requests.Session()
    try:
        # Fazer login
        login_url = f"{base_url}/admin/login"
        login_data = {
            'username': 'admin',
            'password': 'admin123'
        }
        
        response = session.post(login_url, data=login_data, timeout=5)
        print(f"   Status do login: {response.status_code}")
        
        if response.status_code in [200, 302]:
            print("   ✅ Login parece ter funcionado")
            
            # Teste 5: Acessar dashboard após login
            print("\n5️⃣ Testando dashboard após login...")
            dashboard_url = f"{base_url}/admin/dashboard"
            response = session.get(dashboard_url, timeout=5)
            print(f"   Status dashboard: {response.status_code}")
            
            if response.status_code == 200:
                print("   ✅ Dashboard acessível")
                
                # Teste 6: Acessar presentes após login
                print("\n6️⃣ Testando página de presentes após login...")
                presentes_url = f"{base_url}/admin/presentes"
                response = session.get(presentes_url, timeout=5)
                print(f"   Status presentes: {response.status_code}")
                
                if response.status_code == 200:
                    print("   ✅ Página de presentes acessível!")
                    if "presentes" in response.text.lower():
                        print("   ✅ Conteúdo correto encontrado")
                        print(f"\n🎉 TUDO FUNCIONANDO! Acesse: {presentes_url}")
                        return True
                    else:
                        print("   ⚠️ Conteúdo pode estar incorreto")
                        print("   🔍 Primeiros 200 caracteres:")
                        print(f"   {response.text[:200]}")
                else:
                    print(f"   ❌ Erro ao acessar presentes: {response.status_code}")
            else:
                print(f"   ❌ Erro ao acessar dashboard: {response.status_code}")
        else:
            print(f"   ❌ Erro no login: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Erro no teste de login: {e}")
    
    # URLs de referência
    print(f"\n📋 URLS PARA TESTAR MANUALMENTE:")
    print(f"   🌐 Servidor: {base_url}")
    print(f"   🔐 Login: {base_url}/admin/login")
    print(f"   📊 Dashboard: {base_url}/admin/dashboard") 
    print(f"   🎁 Presentes: {base_url}/admin/presentes")
    
    return False

if __name__ == "__main__":
    sucesso = diagnosticar_acesso()
    
    if not sucesso:
        print(f"\n💥 PROBLEMA IDENTIFICADO!")
        print("   1. Certifique-se que o servidor está rodando: python run.py")
        print("   2. Acesse http://127.0.0.1:5000/admin/login no navegador")
        print("   3. Faça login com: admin / admin123")
        print("   4. Navegue para: http://127.0.0.1:5000/admin/presentes")
        print("   5. Se ainda não funcionar, limpe o cache do navegador")
        sys.exit(1)
