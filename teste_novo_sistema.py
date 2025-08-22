"""
Teste do novo sistema de adicionar presentes por link
"""

import requests
import time

def teste_sistema_presente_link():
    """Testa o novo sistema de adicionar presentes por link"""
    
    print("🎁 TESTE DO SISTEMA DE ADICIONAR PRESENTES POR LINK")
    print("=" * 60)
    
    session = requests.Session()
    
    # 1. Fazer login
    print("🔐 Fazendo login...")
    login_data = {'username': 'master', 'password': 'master123'}
    login_response = session.post("http://localhost:5000/admin/login", data=login_data)
    
    if "dashboard" not in login_response.url:
        print("❌ Falha no login")
        return
    
    print("✅ Login realizado com sucesso")
    
    # 2. Testar busca de produto
    print("\n🔍 Testando busca de produto por link...")
    
    # Link de teste (Amazon)
    link_teste = "https://www.amazon.com.br/dp/B08N5WRWNW"  # Echo Dot
    
    busca_data = {
        "link": link_teste
    }
    
    busca_response = session.post(
        "http://localhost:5000/admin/buscar-produto-por-link",
        json=busca_data
    )
    
    print(f"Status da busca: {busca_response.status_code}")
    
    if busca_response.status_code == 200:
        resultado = busca_response.json()
        print(f"Sucesso na busca: {resultado.get('success')}")
        
        if resultado.get('success'):
            print("✅ Informações extraídas:")
            print(f"   📦 Nome: {resultado.get('nome', 'N/A')}")
            print(f"   💰 Preço: {resultado.get('preco', 'N/A')}")
            print(f"   📝 Descrição: {resultado.get('descricao', 'N/A')[:100]}...")
            print(f"   🖼️  Imagem: {resultado.get('imagem', 'N/A')[:50]}...")
            print(f"   🏷️  Categoria: {resultado.get('categoria', 'N/A')}")
            
            # 3. Testar adição do presente
            print("\n➕ Testando adição do presente...")
            
            adicionar_response = session.post(
                "http://localhost:5000/admin/adicionar-presente-por-link",
                json=resultado
            )
            
            if adicionar_response.status_code == 200:
                add_resultado = adicionar_response.json()
                print(f"Sucesso na adição: {add_resultado.get('success')}")
                
                if add_resultado.get('success'):
                    print("🎉 Presente adicionado com sucesso!")
                    print(f"   ID do presente: {add_resultado.get('presente_id')}")
                else:
                    print(f"❌ Erro na adição: {add_resultado.get('error')}")
            else:
                print(f"❌ Erro na requisição de adição: {adicionar_response.status_code}")
        else:
            print(f"❌ Erro na busca: {resultado.get('error')}")
    else:
        print(f"❌ Erro na requisição de busca: {busca_response.status_code}")

def main():
    print("🚀 TESTE DO SISTEMA DE PRESENTES POR LINK")
    print("=" * 50)
    
    time.sleep(2)  # Aguardar servidor
    
    # Teste básico
    teste_sistema_presente_link()
    
    print("\n" + "=" * 50)
    print("📋 PARA TESTAR MANUALMENTE:")
    print("✅ Sistema implementado!")
    print("🔧 Para usar:")
    print("   1. Acesse: http://localhost:5000/admin/presentes")
    print("   2. Faça login (master/master123)")
    print("   3. Clique em 'Adicionar Presente'")
    print("   4. Cole qualquer link de produto")
    print("   5. Clique em 'Buscar Informações'")
    print("   6. Confira e clique em 'Adicionar Presente'")
    print("\n🎉 Agora é muito mais fácil!")

if __name__ == "__main__":
    main()
