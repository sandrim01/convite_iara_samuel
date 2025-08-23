import requests
import time

def verificar_acesso_admin():
    print("🔍 Verificando acesso à página admin...")
    
    base_url = "http://127.0.0.1:5000"
    session = requests.Session()
    
    try:
        # 1. Tentar acessar admin sem login
        print("\n1️⃣ Testando acesso sem login...")
        response = session.get(f"{base_url}/admin/presentes")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 302:
            print("✅ Redirecionamento correto (não logado)")
        elif response.status_code == 200:
            print("⚠️ Página carregou sem login - possível problema de segurança")
            
        # 2. Fazer login
        print("\n2️⃣ Fazendo login...")
        login_data = {'username': 'master', 'password': 'master123'}
        login_response = session.post(f"{base_url}/admin/login", data=login_data)
        print(f"Login status: {login_response.status_code}")
        
        if login_response.status_code in [200, 302]:
            print("✅ Login realizado")
        else:
            print("❌ Falha no login")
            return
            
        # 3. Acessar admin depois do login
        print("\n3️⃣ Acessando admin após login...")
        admin_response = session.get(f"{base_url}/admin/presentes")
        print(f"Admin status: {admin_response.status_code}")
        
        if admin_response.status_code == 200:
            print("✅ Página admin carregada")
            
            # Verificar elementos específicos
            html = admin_response.text
            
            checks = [
                ("CSS principal", "/static/css/style.css" in html),
                ("Hero admin", "hero-admin" in html),
                ("Stats grid", "stats-grid" in html),
                ("Gifts grid", "gifts-grid" in html),
                ("Modal", "modal-adicionar" in html),
                ("JavaScript", "abrirModalAdicionarPresente" in html),
                ("Font Awesome", "fas fa-" in html),
                ("Variáveis CSS", "var(--primary-color)" in html)
            ]
            
            print("\n📊 VERIFICAÇÕES:")
            for nome, resultado in checks:
                status = "✅" if resultado else "❌"
                print(f"{status} {nome}")
                
            # Salvar para análise
            with open('debug_final_admin.html', 'w', encoding='utf-8') as f:
                f.write(html)
            print("\n💾 HTML salvo em debug_final_admin.html")
            
        else:
            print("❌ Erro ao carregar página admin")
            
    except requests.exceptions.ConnectionError:
        print("❌ Servidor não está rodando!")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    verificar_acesso_admin()
