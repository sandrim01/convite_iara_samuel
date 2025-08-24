#!/usr/bin/env python3

import requests

def testar_pagina_restaurada():
    """Testa se a página de presentes foi restaurada corretamente"""
    session = requests.Session()
    
    try:
        print('=== TESTE PÁGINA PRESENTES RESTAURADA ===')
        
        # Fazer login
        login_response = session.post('http://127.0.0.1:5000/admin/login', 
                                    data={'username': 'admin', 'password': 'Casamento2025*#'})
        print(f'Login: {login_response.status_code}')
        
        # Acessar página de presentes
        presentes_response = session.get('http://127.0.0.1:5000/admin/presentes')
        print(f'Presentes: {presentes_response.status_code}')
        
        if presentes_response.status_code == 200:
            content = presentes_response.text
            print('✅ Página carregada com sucesso!')
            
            # Verificar elementos essenciais
            checks = [
                ('CSS presente', '<style>' in content),
                ('Template completo', 'admin-container' in content),
                ('Botão excluir vermelho', 'btn-danger' in content),
                ('Funcionalidade excluir', 'excluirPresente' in content),
                ('Grid de presentes', 'gifts-grid' in content),
                ('FontAwesome', 'fas fa-trash' in content)
            ]
            
            for name, check in checks:
                status = '✅' if check else '❌'
                print(f'{status} {name}')
                
            print('\n📋 RESUMO:')
            if all(check for _, check in checks):
                print('🎉 PÁGINA TOTALMENTE RESTAURADA!')
                print('   - CSS completo carregado')
                print('   - Botão excluir com cor vermelha')
                print('   - Todas as funcionalidades presentes')
            else:
                print('⚠️ ALGUNS PROBLEMAS AINDA EXISTEM')
                
        else:
            print(f'❌ Erro ao acessar página: {presentes_response.status_code}')
            
    except Exception as e:
        print(f'❌ Erro durante teste: {e}')

if __name__ == "__main__":
    testar_pagina_restaurada()
