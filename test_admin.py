import requests
import sys

# URL da aplicação
BASE_URL = "http://127.0.0.1:5000"

def test_admin_login():
    print("🔍 Testando painel administrativo...")
    
    # Teste 1: Verificar se a página de login carrega
    try:
        response = requests.get(f"{BASE_URL}/admin/login", timeout=5)
        print(f"✅ Página de login: Status {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ Erro: Página de login retornou status {response.status_code}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Erro ao acessar página de login: {e}")
        return False
    
    # Teste 2: Tentar fazer login
    session = requests.Session()
    
    try:
        # Primeiro, obter a página de login para manter a sessão
        login_page = session.get(f"{BASE_URL}/admin/login", timeout=5)
        
        # Fazer login
        login_data = {
            'username': 'admin',
            'password': 'admin'
        }
        
        response = session.post(f"{BASE_URL}/admin/login", data=login_data, timeout=5)
        
        if response.status_code == 200 and "dashboard" in response.url:
            print("✅ Login realizado com sucesso!")
            print(f"📊 Redirecionado para: {response.url}")
            return True
        elif response.status_code == 302:
            print("✅ Login redirecionou corretamente!")
            return True
        else:
            print(f"❌ Login falhou: Status {response.status_code}")
            print(f"URL atual: {response.url}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Erro durante login: {e}")
        return False

def test_admin_dashboard():
    print("\n🏠 Testando dashboard...")
    
    session = requests.Session()
    
    try:
        # Fazer login primeiro
        login_data = {
            'username': 'admin',
            'password': 'admin'
        }
        
        session.post(f"{BASE_URL}/admin/login", data=login_data, timeout=5)
        
        # Acessar dashboard
        response = session.get(f"{BASE_URL}/admin/dashboard", timeout=5)
        
        if response.status_code == 200:
            print("✅ Dashboard carregou com sucesso!")
            return True
        else:
            print(f"❌ Dashboard falhou: Status {response.status_code}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Erro ao acessar dashboard: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando testes do painel administrativo...\n")
    
    # Verificar se o servidor está rodando
    try:
        response = requests.get(BASE_URL, timeout=5)
        print(f"✅ Servidor está rodando: Status {response.status_code}\n")
    except requests.RequestException:
        print("❌ Servidor não está rodando!")
        print("Execute 'python run.py' primeiro!")
        sys.exit(1)
    
    # Executar testes
    login_ok = test_admin_login()
    dashboard_ok = test_admin_dashboard()
    
    print("\n" + "="*50)
    print("📋 RESULTADO DOS TESTES:")
    print(f"Login: {'✅ OK' if login_ok else '❌ FALHOU'}")
    print(f"Dashboard: {'✅ OK' if dashboard_ok else '❌ FALHOU'}")
    
    if login_ok and dashboard_ok:
        print("\n🎉 Painel administrativo está funcionando perfeitamente!")
        print("👤 Use as credenciais: admin/admin")
    else:
        print("\n⚠️ Há problemas no painel administrativo.")
