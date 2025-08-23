import requests
from bs4 import BeautifulSoup

def capturar_html_admin():
    session = requests.Session()
    
    # Login
    login_data = {'username': 'master', 'password': 'master123'}
    session.post('http://127.0.0.1:5000/admin/login', data=login_data)
    
    # Buscar página de presentes
    response = session.get('http://127.0.0.1:5000/admin/presentes')
    
    # Salvar HTML completo
    with open('debug_presentes_completo.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    
    # Analisar
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Verificar CSS
    print("=== ANÁLISE CSS ===")
    
    # Verificar link para CSS principal
    css_link = soup.find('link', href=lambda x: x and 'style.css' in x)
    print(f"CSS principal: {css_link.get('href') if css_link else 'NÃO ENCONTRADO'}")
    
    # Verificar se existe bloco style
    style_blocks = soup.find_all('style')
    print(f"Blocos de style: {len(style_blocks)}")
    
    if style_blocks:
        # Verificar se variáveis CSS estão sendo usadas
        style_content = str(style_blocks[0]) if style_blocks else ""
        print(f"Usa --primary-color: {'--primary-color' in style_content}")
        print(f"Usa --secondary-color: {'--secondary-color' in style_content}")
        print(f"Usa var(): {'var(' in style_content}")
    
    # Verificar se hero-admin está presente
    hero_admin = soup.find(class_='hero-admin')
    print(f"Hero admin presente: {hero_admin is not None}")
    
    if hero_admin:
        # Verificar se tem estilo inline aplicado
        print(f"Hero admin tem style: {hero_admin.get('style', 'Não')}")
    
    print("HTML salvo em: debug_presentes_completo.html")

if __name__ == "__main__":
    capturar_html_admin()
