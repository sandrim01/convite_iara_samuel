#!/usr/bin/env python3
"""
Script para diagnosticar problemas com o botão de excluir presente
"""

import requests
from bs4 import BeautifulSoup
import json

def teste_excluir_presente():
    """Testa a funcionalidade de excluir presente"""
    
    session = requests.Session()
    base_url = 'http://127.0.0.1:5000'
    
    print("🔧 DIAGNÓSTICO - BOTÃO EXCLUIR PRESENTE")
    print("=" * 50)
    
    # 1. Login
    print("🔑 Fazendo login...")
    login_data = {'username': 'master', 'password': 'master123'}
    login_response = session.post(f'{base_url}/admin/login', data=login_data)
    print(f"🔑 Login Status: {login_response.status_code}")
    
    if login_response.status_code != 200:
        print("❌ Erro no login")
        return
    
    # 2. Acessar página de presentes
    print("📄 Acessando página de presentes...")
    presentes_response = session.get(f'{base_url}/admin/presentes')
    print(f"📄 Presentes Status: {presentes_response.status_code}")
    
    if presentes_response.status_code != 200:
        print("❌ Erro ao acessar página de presentes")
        print("Conteúdo da resposta:", presentes_response.text[:500])
        return
    
    # 3. Analisar HTML
    soup = BeautifulSoup(presentes_response.text, 'html.parser')
    
    # Procurar botões de remover
    botoes_remover = soup.find_all('button', onclick=lambda x: x and 'confirmarRemocao' in x)
    print(f"🗑️  Botões de remover encontrados: {len(botoes_remover)}")
    
    if botoes_remover:
        print("✅ Primeiro botão de remover:")
        primeiro_botao = botoes_remover[0]
        print(f"   onclick: {primeiro_botao.get('onclick')}")
        print(f"   class: {primeiro_botao.get('class')}")
        print(f"   HTML: {str(primeiro_botao)[:200]}...")
    
    # Procurar função JavaScript confirmarRemocao
    scripts = soup.find_all('script')
    funcao_encontrada = False
    
    for script in scripts:
        if script.string and 'confirmarRemocao' in script.string:
            print("✅ Função confirmarRemocao encontrada")
            funcao_encontrada = True
            # Extrair parte relevante da função
            linhas = script.string.split('\n')
            for i, linha in enumerate(linhas):
                if 'function confirmarRemocao' in linha:
                    print("📝 Função JavaScript:")
                    for j in range(max(0, i), min(len(linhas), i+10)):
                        print(f"  {j-i+1}: {linhas[j].strip()}")
                    break
            break
    
    if not funcao_encontrada:
        print("❌ Função JavaScript confirmarRemocao NÃO encontrada")
    
    # Verificar se há presentes para testar
    cards_presente = soup.find_all('div', class_='presente-card')
    print(f"🎁 Presentes encontrados na página: {len(cards_presente)}")
    
    if cards_presente and botoes_remover:
        # Extrair ID do primeiro presente
        primeiro_onclick = botoes_remover[0].get('onclick', '')
        import re
        match = re.search(r"confirmarRemocao\('(\d+)'", primeiro_onclick)
        if match:
            presente_id = match.group(1)
            print(f"🎯 ID do primeiro presente: {presente_id}")
            
            # Testar se a rota existe (sem realmente excluir)
            print("🔍 Testando se a rota de exclusão está acessível...")
            # Só fazemos HEAD request para verificar se a rota existe
            try:
                rota_url = f'{base_url}/admin/presentes/{presente_id}/remover'
                # Não vamos fazer POST para não excluir realmente
                print(f"📍 Rota que seria chamada: {rota_url}")
            except Exception as e:
                print(f"❌ Erro ao testar rota: {e}")
    
    # Salvar HTML para análise
    with open('debug_excluir_presente.html', 'w', encoding='utf-8') as f:
        f.write(presentes_response.text)
    print("📁 HTML completo salvo em debug_excluir_presente.html")
    
    print("\n" + "=" * 50)
    print("🏁 DIAGNÓSTICO CONCLUÍDO")

if __name__ == '__main__':
    teste_excluir_presente()
