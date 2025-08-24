import requests
import sys

def diagnosticar_acesso_presentes():
    """Diagnostica problemas de acesso à página de gerenciar presentes"""
    base_url = "http://127.0.0.1:5000"
    session = requests.Session()
    
    print("🔍 DIAGNÓSTICO: ACESSO À PÁGINA DE PRESENTES\n")
    
    try:
        # 1. Verificar se o servidor está respondendo
        print("1️⃣ Verificando se servidor está ativo...")
        try:
            response = session.get(base_url, timeout=5)
            print(f"✅ Servidor ativo - Status: {response.status_code}")
        except Exception as e:
            print(f"❌ Servidor não responde: {e}")
            return False
        
        # 2. Tentar acessar página de presentes sem login
        print("\n2️⃣ Testando acesso sem login...")
        presentes_url = f"{base_url}/admin/presentes"
        response = session.get(presentes_url, timeout=5)
        print(f"Status sem login: {response.status_code}")
        
        if response.status_code == 200:
            print("⚠️ Acesso permitido sem login (possível problema de segurança)")
        elif response.status_code == 302:
            print("✅ Redirecionamento detectado (provavelmente para login)")
        elif response.status_code == 401:
            print("✅ Acesso negado - autenticação necessária")
        else:
            print(f"❌ Status inesperado: {response.status_code}")
        
        # 3. Fazer login com a senha correta
        print("\n3️⃣ Fazendo login com credenciais corretas...")
        login_url = f"{base_url}/admin/login"
        login_data = {
            'username': 'admin',
            'password': 'Casamento2025*#'  # Senha correta identificada
        }
        
        login_response = session.post(login_url, data=login_data, timeout=5)
        print(f"Login status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            # Verificar se login foi bem-sucedido analisando a resposta
            if "dashboard" in login_response.text.lower() or "painel" in login_response.text.lower():
                print("✅ Login realizado com sucesso!")
            else:
                print("⚠️ Login pode ter falhado - verificar credenciais")
        elif login_response.status_code == 302:
            print("✅ Login com redirecionamento (provavelmente sucesso)")
        else:
            print(f"❌ Erro no login: {login_response.status_code}")
        
        # 4. Tentar acessar página de presentes após login
        print("\n4️⃣ Testando acesso à página de presentes após login...")
        presentes_response = session.get(presentes_url, timeout=5)
        print(f"Status após login: {presentes_response.status_code}")
        
        if presentes_response.status_code == 200:
            print("✅ Página de presentes acessível!")
            
            # Verificar conteúdo da página
            content = presentes_response.text
            checks = [
                ("Título da página", "presentes" in content.lower()),
                ("Campo de link", "link" in content.lower()),
                ("Botão adicionar", "adicionar" in content.lower()),
                ("JavaScript funcional", "adicionarPresentePorLink" in content)
            ]
            
            print("\n📋 Verificação do conteúdo:")
            for name, check in checks:
                status = "✅" if check else "❌"
                print(f"   {status} {name}")
                
            return True
        else:
            print(f"❌ Não conseguiu acessar página de presentes: {presentes_response.status_code}")
            
            # Verificar se está sendo redirecionado
            if presentes_response.status_code == 302:
                location = presentes_response.headers.get('Location', 'N/A')
                print(f"🔄 Redirecionamento para: {location}")
            
            return False
    
    except Exception as e:
        print(f"❌ Erro durante diagnóstico: {e}")
        return False

def verificar_rotas_admin():
    """Verifica se as rotas admin estão funcionando"""
    print("\n🔍 VERIFICAÇÃO DE ROTAS ADMIN")
    
    base_url = "http://127.0.0.1:5000"
    session = requests.Session()
    
    # Fazer login primeiro
    login_data = {
        'username': 'admin',
        'password': 'Casamento2025*#'
    }
    session.post(f"{base_url}/admin/login", data=login_data)
    
    # Testar rotas admin principais
    rotas_teste = [
        ("/admin", "Dashboard"),
        ("/admin/dashboard", "Dashboard alternativo"),
        ("/admin/presentes", "Gerenciar Presentes"),
        ("/admin/convidados", "Gerenciar Convidados"),
        ("/admin/configuracoes", "Configurações")
    ]
    
    for rota, nome in rotas_teste:
        try:
            response = session.get(f"{base_url}{rota}", timeout=5)
            status = "✅" if response.status_code == 200 else "❌"
            print(f"   {status} {nome} ({rota}): {response.status_code}")
        except Exception as e:
            print(f"   ❌ {nome} ({rota}): Erro - {e}")

if __name__ == "__main__":
    print("🚨 DIAGNÓSTICO COMPLETO - ACESSO PRESENTES\n")
    
    # Executar diagnósticos
    acesso_ok = diagnosticar_acesso_presentes()
    verificar_rotas_admin()
    
    print(f"\n📊 RESULTADO FINAL:")
    if acesso_ok:
        print("🎉 PÁGINA DE PRESENTES ACESSÍVEL!")
        print("💡 Acesse: http://127.0.0.1:5000/admin/login")
        print("🔐 Use: admin / Casamento2025*#")
        print("📝 Depois vá para: http://127.0.0.1:5000/admin/presentes")
    else:
        print("💥 PROBLEMA IDENTIFICADO!")
        print("🔧 Verifique:")
        print("   1. Servidor está rodando?")
        print("   2. Credenciais estão corretas?")
        print("   3. URL está correta?")
        print("   4. Não há erros no console do navegador?")
