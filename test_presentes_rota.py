from app import create_app
from app.models import Presente, ConfiguracaoSite

def test_presentes_route():
    app = create_app()
    
    with app.test_client() as client:
        with app.app_context():
            # Verificar dados
            presentes = Presente.query.filter_by(disponivel=True).all()
            print(f"Presentes no banco: {len(presentes)}")
            
            # Testar rota
            response = client.get('/presentes')
            print(f"Status da resposta: {response.status_code}")
            
            if response.status_code == 200:
                content = response.get_data(as_text=True)
                print(f"Tamanho do conteúdo HTML: {len(content)} caracteres")
                
                # Verificar se tem os presentes no HTML
                if "gift-card" in content:
                    print("✅ Cards de presentes encontrados no HTML")
                else:
                    print("❌ Cards de presentes NÃO encontrados no HTML")
                
                # Verificar alguns nomes de presentes
                presentes_nomes = [p.nome for p in presentes[:3]]
                encontrados = 0
                for nome in presentes_nomes:
                    if nome in content:
                        encontrados += 1
                        print(f"✅ Presente '{nome}' encontrado no HTML")
                    else:
                        print(f"❌ Presente '{nome}' NÃO encontrado no HTML")
                
                print(f"Total encontrados: {encontrados}/{len(presentes_nomes)}")
            else:
                print(f"❌ Erro na rota: {response.status_code}")

if __name__ == "__main__":
    test_presentes_route()
