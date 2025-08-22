"""
Teste completo da exclusão de presentes com login automático
"""

import requests
import time

def fazer_login():
    """Faz login automático no sistema"""
    session = requests.Session()
    
    print("🔐 Fazendo login no sistema...")
    
    # Primeiro, pegar a página de login para verificar se existe CSRF token
    login_page = session.get("http://localhost:5000/admin/login")
    
    # Dados de login (usando credenciais do usuário master)
    login_data = {
        'username': 'master',
        'password': 'master123'
    }
    
    # Fazer login
    response = session.post("http://localhost:5000/admin/login", data=login_data)
    
    if response.status_code == 200 and "/admin/dashboard" in response.url:
        print("   ✅ Login realizado com sucesso!")
        return session
    else:
        print(f"   ❌ Falha no login - Status: {response.status_code}")
        print(f"   URL final: {response.url}")
        return None

def verificar_presentes_com_login():
    """Verifica presentes após fazer login"""
    
    # Fazer login
    session = fazer_login()
    if not session:
        print("❌ Não foi possível fazer login. Verifique as credenciais.")
        return
    
    print("\n📦 Verificando presentes após login...")
    
    # Acessar página de presentes
    response = session.get("http://localhost:5000/admin/presentes")
    
    if response.status_code == 200:
        print(f"   ✅ Página carregada - Status: {response.status_code}")
        
        # Verificar se tem presentes
        if "presente-card" in response.text:
            print("   ✅ Presentes encontrados!")
            
            # Extrair IDs
            import re
            ids = re.findall(r"onclick=\"confirmarRemocao\('(\d+)'", response.text)
            print(f"   📋 IDs encontrados: {ids}")
            
            if "confirmarRemocao" in response.text:
                print("   ✅ Função JavaScript presente")
            
            if "btn-danger" in response.text:
                print("   ✅ Botões de remoção encontrados")
                
            return session, ids
        else:
            print("   ⚠️  Nenhum presente cadastrado")
            print("   💡 Vamos adicionar um presente para teste...")
            
            # Adicionar presente para teste
            adicionar_presente_teste(session)
            return None, []
    else:
        print(f"   ❌ Erro ao acessar página - Status: {response.status_code}")
        return None, []

def adicionar_presente_teste(session):
    """Adiciona um presente para teste"""
    
    print("\n➕ Adicionando presente para teste...")
    
    presente_data = {
        'nome': 'Presente Teste para Exclusão',
        'categoria': 'casa',
        'descricao': 'Este é um presente de teste que será excluído',
        'preco_sugerido': '50.00',
        'link_loja': 'https://exemplo.com',
        'disponivel': True
    }
    
    response = session.post("http://localhost:5000/admin/adicionar_presente", data=presente_data)
    
    if response.status_code == 200:
        print("   ✅ Presente de teste adicionado!")
        return True
    else:
        print(f"   ❌ Erro ao adicionar presente - Status: {response.status_code}")
        return False

def testar_exclusao_presente(session, presente_id):
    """Testa a exclusão de um presente específico"""
    
    print(f"\n🗑️  Testando exclusão do presente ID: {presente_id}")
    
    # Simular a requisição que o JavaScript faria
    response = session.post(f"http://localhost:5000/admin/presentes/{presente_id}/remover")
    
    if response.status_code == 200:
        print("   ✅ Requisição de exclusão bem-sucedida!")
        
        # Verificar se foi redirecionado para a lista
        if "presentes" in response.url:
            print("   ✅ Redirecionamento correto para lista de presentes")
        
        return True
    else:
        print(f"   ❌ Erro na exclusão - Status: {response.status_code}")
        return False

def main():
    print("🚀 TESTE COMPLETO DE EXCLUSÃO DE PRESENTES")
    print("=" * 60)
    
    # Aguardar servidor
    print("⏳ Aguardando servidor...")
    time.sleep(2)
    
    # Verificar presentes com login
    session, ids = verificar_presentes_com_login()
    
    if session and ids:
        print(f"\n🎯 Testando exclusão com o primeiro presente: {ids[0]}")
        sucesso = testar_exclusao_presente(session, ids[0])
        
        if sucesso:
            print("\n✅ TESTE CONCLUÍDO COM SUCESSO!")
            print("🎉 A funcionalidade de exclusão está funcionando!")
        else:
            print("\n❌ TESTE FALHOU!")
            print("🔧 Verificar logs do servidor para mais detalhes")
    else:
        print("\n⚠️  Não foi possível completar o teste")
        print("💡 Certifique-se de que:")
        print("   - O servidor está rodando")
        print("   - Existe um usuário admin/admin123")
        print("   - Existem presentes cadastrados")

if __name__ == "__main__":
    main()
