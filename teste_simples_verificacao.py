#!/usr/bin/env python3

import requests
import time

def teste_simples():
    """Teste simples da página de presentes"""
    print('=== TESTE SIMPLES ===')
    
    # Aguardar servidor estabilizar
    time.sleep(3)
    
    session = requests.Session()
    
    try:
        # Login
        login_response = session.post('http://127.0.0.1:5000/admin/login', 
                                    data={'username': 'admin', 'password': 'Casamento2025*#'}, 
                                    timeout=15)
        print(f'Login: {login_response.status_code}')
        
        # Página presentes
        presentes_response = session.get('http://127.0.0.1:5000/admin/presentes', timeout=15)
        print(f'Presentes: {presentes_response.status_code}')
        
        if presentes_response.status_code == 200:
            content = presentes_response.text
            
            # Verificações básicas
            checks = {
                'Campo link': 'id="linkPresente"' in content,
                'Botão adicionar': 'btnAdicionarLink' in content,
                'Função JS': 'adicionarPresentePorLink' in content,
                'Botão excluir vermelho': 'btn-danger' in content,
                'CSS presente': '<style>' in content
            }
            
            print('\n📋 VERIFICAÇÕES:')
            for name, check in checks.items():
                status = '✅' if check else '❌'
                print(f'{status} {name}')
            
            return all(checks.values())
        else:
            print('❌ Erro ao acessar página')
            return False
            
    except Exception as e:
        print(f'❌ Erro: {e}')
        return False

if __name__ == "__main__":
    sucesso = teste_simples()
    print(f'\n🎯 RESULTADO: {"TUDO OK" if sucesso else "PRECISA AJUSTAR"}')
