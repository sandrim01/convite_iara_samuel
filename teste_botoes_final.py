import requests

# Teste final para verificar os botões
session = requests.Session()

# Fazer login
login_url = "http://127.0.0.1:5000/admin/login"
login_data = {
    'username': 'master',
    'password': 'master123'
}

try:
    # Login
    login_response = session.post(login_url, data=login_data)
    print(f"Login Status: {login_response.status_code}")
    
    # Acessar página de presentes
    presentes_url = "http://127.0.0.1:5000/admin/presentes"
    response = session.get(presentes_url)
    print(f"Presentes Status: {response.status_code}")
    
    # Verificar botão do cabeçalho
    if 'onclick="abrirModalAdicionarPresente()"' in response.text:
        print("✅ Botão do cabeçalho encontrado")
    else:
        print("❌ Botão do cabeçalho NÃO encontrado")
    
    # Verificar se não tem mais o botão de baixo
    if "Adicionar Primeiro Presente" in response.text:
        print("❌ Botão de baixo ainda existe")
    else:
        print("✅ Botão de baixo removido com sucesso")
    
    # Verificar função JavaScript
    if "function abrirModalAdicionarPresente()" in response.text:
        print("✅ Função JavaScript encontrada")
    else:
        print("❌ Função JavaScript NÃO encontrada")
    
    # Verificar modal
    if 'id="modalAdicionarPresente"' in response.text:
        print("✅ Modal encontrado")
    else:
        print("❌ Modal NÃO encontrado")
    
    # Contar quantos botões existem
    count_botoes = response.text.count('onclick="abrirModalAdicionarPresente()"')
    print(f"📊 Total de botões que chamam abrirModalAdicionarPresente(): {count_botoes}")
    
    # Verificar texto atualizado
    if "Use o botão \"Adicionar Presente\" acima para começar!" in response.text:
        print("✅ Texto atualizado encontrado")
    else:
        print("❌ Texto NÃO foi atualizado")
    
    print("\n📄 Salvando HTML para análise...")
    with open('debug_presentes_final.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    print("HTML salvo em debug_presentes_final.html")
    
except Exception as e:
    print(f"Erro: {e}")
