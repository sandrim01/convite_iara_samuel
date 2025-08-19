import requests
import sys

# URL da aplicação
BASE_URL = "http://127.0.0.1:5000"

def test_confirmation():
    print("🔍 Testando confirmação de presença...")
    
    session = requests.Session()
    
    try:
        # Primeiro, obter a página local para manter a sessão
        response = session.get(f"{BASE_URL}/local", timeout=10)
        print(f"✅ Página local carregou: Status {response.status_code}")
        
        # Dados de teste para confirmação
        confirmation_data = {
            'nome': 'João Teste',
            'telefone': '(11) 99999-9999',
            'email': 'joao@teste.com',
            'acompanhantes': '1',
            'observacoes': 'Teste de confirmação'
        }
        
        print("📝 Enviando dados de confirmação...")
        print(f"Dados: {confirmation_data}")
        
        # Enviar confirmação
        response = session.post(f"{BASE_URL}/processar-confirmacao", 
                              data=confirmation_data, 
                              timeout=10,
                              allow_redirects=False)
        
        print(f"Status da resposta: {response.status_code}")
        print(f"Headers: {response.headers}")
        
        if response.status_code == 302:
            print(f"✅ Redirecionamento para: {response.headers.get('Location', 'N/A')}")
            
            # Seguir o redirecionamento
            redirect_response = session.get(response.headers.get('Location', ''), timeout=10)
            print(f"✅ Página final: Status {redirect_response.status_code}")
            
            return True
        elif response.status_code == 500:
            print("❌ Erro 500 - Internal Server Error")
            print(f"Conteúdo da resposta: {response.text[:500]}")
            return False
        else:
            print(f"⚠️ Status inesperado: {response.status_code}")
            print(f"Conteúdo: {response.text[:500]}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Erro na requisição: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando teste de confirmação de presença...\n")
    
    # Verificar se o servidor está rodando
    try:
        response = requests.get(BASE_URL, timeout=5)
        print(f"✅ Servidor está rodando: Status {response.status_code}\n")
    except requests.RequestException:
        print("❌ Servidor não está rodando!")
        print("Execute 'python run.py' primeiro!")
        sys.exit(1)
    
    # Executar teste
    success = test_confirmation()
    
    print("\n" + "="*50)
    if success:
        print("🎉 Teste de confirmação passou!")
    else:
        print("❌ Teste de confirmação falhou!")
        print("Verifique os logs do servidor para mais detalhes.")
