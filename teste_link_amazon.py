#!/usr/bin/env python3

import requests
import json

def testar_link_especifico():
    """Testa o link específico fornecido pelo usuário"""
    
    link = "https://www.amazon.com.br/C%C3%B4moda-Dit%C3%A1lia-Gavetas-Dm-243-Verde/dp/B0DD5G8CD5/ref=sr_1_1_sspa?_encoding=UTF8&dib=eyJ2IjoiMSJ9.FDEGYiE0IJIpCpxmIY1H3KW2umDMyGKAiokHCiRWkdrU3p-RR9DY0LJnanE4m06O9bw6AtYySJxziwXQgKBD51jBw1q5hSINMSPMOEFK51lSalBcAquk1D_bHdoJkjx2h2YsQ8VCzG1K677zb2KTqgugaXjO51HYKY8czeL6sUJ1gCxYOOj1cnjNulLaLfzraQWZqNDxR2BjA6L9q1xkuCjcah12O6IwZkLuvA4zta4.j-9042cbxfebJIK9Hj17aWxneFzPwqZ2o2crWN795Q0&dib_tag=se&keywords=comoda+%7C+gaveteiro&qid=1756036452&s=home-furnishings&sr=1-1-spons&ufe=app_do%3Aamzn1.fos.25548f35-0de7-44b3-b28e-0f56f3f96147&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1"
    
    session = requests.Session()
    
    try:
        print('=== TESTE COM LINK ESPECÍFICO ===')
        print(f'Link: {link[:100]}...')
        
        # Login
        print('\n🔐 Fazendo login...')
        login_response = session.post('http://127.0.0.1:5000/admin/login', 
                                    data={'username': 'admin', 'password': 'Casamento2025*#'}, 
                                    timeout=10)
        print(f'Status login: {login_response.status_code}')
        
        if login_response.status_code not in [200, 302]:
            print('❌ Falha no login')
            return False
        
        # Testar adição
        print('\n🔗 Testando adição do produto Amazon...')
        
        test_data = {'link': link}
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        print('Enviando requisição...')
        response = session.post('http://127.0.0.1:5000/admin/adicionar-presente-por-link', 
                              json=test_data, 
                              headers=headers, 
                              timeout=30)  # Timeout maior para Amazon
        
        print(f'Status da resposta: {response.status_code}')
        print(f'Headers da resposta: {dict(response.headers)}')
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f'📋 Resposta JSON: {result}')
                
                if result.get('success'):
                    print('✅ Produto adicionado com sucesso!')
                    print(f'   ID: {result.get("presente_id")}')
                    print(f'   Mensagem: {result.get("message")}')
                    if result.get('warning'):
                        print(f'   ⚠️ Aviso: {result.get("warning")}')
                    return True
                else:
                    print(f'❌ Erro na adição: {result.get("error", "Erro desconhecido")}')
                    return False
                    
            except json.JSONDecodeError as e:
                print(f'❌ Erro ao decodificar JSON: {e}')
                print(f'Conteúdo bruto da resposta: {response.text[:500]}')
                return False
        else:
            print(f'❌ Erro HTTP {response.status_code}')
            print(f'Conteúdo da resposta: {response.text[:500]}')
            return False
            
    except requests.exceptions.Timeout:
        print('❌ Timeout na requisição - Amazon pode estar lenta')
        return False
    except Exception as e:
        print(f'❌ Erro durante teste: {type(e).__name__}: {e}')
        return False

def verificar_servidor():
    """Verifica se o servidor está rodando"""
    try:
        response = requests.get('http://127.0.0.1:5000/', timeout=5)
        print(f'✅ Servidor rodando: {response.status_code}')
        return True
    except:
        print('❌ Servidor não está rodando')
        return False

if __name__ == "__main__":
    print('🧪 TESTE ESPECÍFICO COM LINK AMAZON\n')
    
    if verificar_servidor():
        sucesso = testar_link_especifico()
        print(f'\n🎯 RESULTADO: {"✅ SUCESSO" if sucesso else "❌ FALHA"}')
    else:
        print('\n💡 DICA: Execute "python run.py" para iniciar o servidor')
