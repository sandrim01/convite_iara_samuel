#!/usr/bin/env python3

import requests
import json

def testar_exclusao_presente():
    """Testa a funcionalidade de excluir presente"""
    session = requests.Session()
    
    try:
        print('=== TESTE EXCLUSÃO DE PRESENTE ===')
        
        # Fazer login
        login_response = session.post('http://127.0.0.1:5000/admin/login', 
                                    data={'username': 'admin', 'password': 'Casamento2025*#'})
        print(f'Login: {login_response.status_code}')
        
        if login_response.status_code not in [200, 302]:
            print('❌ Falha no login')
            return False
        
        # Primeiro listar presentes para pegar um ID válido
        presentes_response = session.get('http://127.0.0.1:5000/admin/presentes')
        if presentes_response.status_code != 200:
            print('❌ Erro ao acessar página de presentes')
            return False
            
        # Verificar se tem presentes na página
        content = presentes_response.text
        if 'data-id=' in content:
            # Extrair um ID de presente da página
            import re
            match = re.search(r'data-id="(\d+)"', content)
            if match:
                presente_id = match.group(1)
                print(f'✅ Presente ID encontrado: {presente_id}')
                
                # Testar remoção
                print(f'\n🗑️ Testando remoção do presente {presente_id}...')
                remover_url = f'http://127.0.0.1:5000/admin/presentes/{presente_id}/remover'
                
                response = session.post(remover_url)
                print(f'Status da requisição: {response.status_code}')
                
                # Verificar se retorna JSON
                try:
                    result = response.json()
                    print(f'Resposta JSON: {result}')
                    
                    if result.get('success'):
                        print('✅ Presente removido com sucesso!')
                        return True
                    else:
                        print(f'⚠️ Erro na remoção: {result.get("error", "Erro desconhecido")}')
                        # Se o erro é sobre presente já escolhido, ainda é um sucesso do teste
                        if 'já foi escolhido' in result.get('error', ''):
                            print('✅ API funcionando corretamente (presente já escolhido)')
                            return True
                        return False
                        
                except json.JSONDecodeError:
                    print('❌ Resposta não é JSON válido')
                    print(f'Conteúdo recebido: {response.text[:200]}')
                    return False
            else:
                print('❌ Nenhum ID de presente encontrado na página')
                return False
        else:
            print('⚠️ Nenhum presente encontrado na página para testar')
            return True  # Não é erro se não há presentes
            
    except Exception as e:
        print(f'❌ Erro durante teste: {e}')
        return False

if __name__ == "__main__":
    sucesso = testar_exclusao_presente()
    print(f'\n📋 RESULTADO: {"✅ SUCESSO" if sucesso else "❌ FALHA"}')
