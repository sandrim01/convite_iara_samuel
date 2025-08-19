from app import create_app

app = create_app()

with app.test_request_context('/local'):
    print("🔍 Testando rota local com contexto de requisição...")
    
    try:
        from app.routes.main import local
        response = local()
        print(f"✅ Rota executou com sucesso!")
        print(f"Tipo da resposta: {type(response)}")
        if hasattr(response, 'status_code'):
            print(f"Status: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Erro na rota local: {e}")
        import traceback
        traceback.print_exc()
