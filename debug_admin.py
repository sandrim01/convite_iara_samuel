from app import create_app
from app.models import Admin
from flask import url_for

app = create_app()

with app.app_context():
    # Teste básico de rota
    with app.test_client() as client:
        print("🔍 Testando rota admin/login...")
        
        try:
            response = client.get('/admin/login')
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Página de login carregou com sucesso!")
                print(f"Conteúdo: {len(response.data)} bytes")
            else:
                print(f"❌ Erro: Status {response.status_code}")
                print(f"Dados: {response.data.decode('utf-8')[:500]}")
                
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")
            import traceback
            traceback.print_exc()
            
        print("\n🔍 Testando login...")
        
        try:
            response = client.post('/admin/login', data={
                'username': 'admin',
                'password': 'admin'
            }, follow_redirects=True)
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                if "dashboard" in response.request.path or "painel" in response.data.decode().lower():
                    print("✅ Login realizado com sucesso!")
                else:
                    print("⚠️ Login pode ter falhado - não redirecionou para dashboard")
            else:
                print(f"❌ Erro no login: Status {response.status_code}")
                
        except Exception as e:
            print(f"❌ Erro no login: {e}")
            import traceback
            traceback.print_exc()
