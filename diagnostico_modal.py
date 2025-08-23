import requests
from bs4 import BeautifulSoup

# Teste detalhado do modal
session = requests.Session()

# Login
login_url = "http://127.0.0.1:5000/admin/login"
login_data = {'username': 'master', 'password': 'master123'}

try:
    # Fazer login
    login_response = session.post(login_url, data=login_data)
    print(f"🔑 Login Status: {login_response.status_code}")
    
    # Acessar página de presentes
    presentes_url = "http://127.0.0.1:5000/admin/presentes"
    response = session.get(presentes_url)
    print(f"📄 Presentes Status: {response.status_code}")
    
    # Parse HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 1. Verificar se o botão existe
    botao = soup.find('button', {'onclick': 'abrirModalAdicionarPresente()'})
    if botao:
        print("✅ Botão encontrado:", botao.get_text(strip=True))
    else:
        print("❌ Botão NÃO encontrado")
        # Procurar todos os botões
        todos_botoes = soup.find_all('button')
        print(f"📊 Total de botões na página: {len(todos_botoes)}")
        for i, btn in enumerate(todos_botoes):
            print(f"  {i+1}. {btn.get_text(strip=True)} - onclick: {btn.get('onclick', 'N/A')}")
    
    # 2. Verificar se o modal existe
    modal = soup.find('div', {'id': 'modalAdicionarPresente'})
    if modal:
        print("✅ Modal encontrado")
    else:
        print("❌ Modal NÃO encontrado")
    
    # 3. Verificar se a função JavaScript existe
    scripts = soup.find_all('script')
    funcao_encontrada = False
    for script in scripts:
        if script.string and 'function abrirModalAdicionarPresente' in script.string:
            funcao_encontrada = True
            print("✅ Função JavaScript encontrada")
            # Mostrar a função
            linhas = script.string.split('\n')
            for i, linha in enumerate(linhas):
                if 'function abrirModalAdicionarPresente' in linha:
                    print("📝 Função JavaScript:")
                    for j in range(max(0, i), min(len(linhas), i+10)):
                        print(f"  {j+1}: {linhas[j].strip()}")
                    break
            break
    
    if not funcao_encontrada:
        print("❌ Função JavaScript NÃO encontrada")
        print(f"📊 Total de scripts na página: {len(scripts)}")
    
    # 4. Verificar CSS do modal
    styles = soup.find_all('style')
    css_modal_encontrado = False
    for style in styles:
        if style.string and '.modal' in style.string:
            css_modal_encontrado = True
            print("✅ CSS do modal encontrado")
            break
    
    if not css_modal_encontrado:
        print("❌ CSS do modal NÃO encontrado")
    
    # 5. Salvar HTML para análise detalhada
    with open('debug_modal_completo.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    print("📁 HTML completo salvo em debug_modal_completo.html")
    
except Exception as e:
    print(f"❌ Erro: {e}")
