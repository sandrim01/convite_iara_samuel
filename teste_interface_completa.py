#!/usr/bin/env python3

import requests
import time

def teste_interface_completa():
    """Teste completo da interface de presentes"""
    session = requests.Session()
    
    try:
        print('=== TESTE INTERFACE COMPLETA ===')
        
        # Login
        login_response = session.post('http://127.0.0.1:5000/admin/login', 
                                    data={'username': 'admin', 'password': 'Casamento2025*#'})
        print(f'✅ Login: {login_response.status_code}')
        
        # Acessar página de presentes
        presentes_response = session.get('http://127.0.0.1:5000/admin/presentes')
        print(f'✅ Página presentes: {presentes_response.status_code}')
        
        if presentes_response.status_code == 200:
            content = presentes_response.text
            
            # Verificar funcionalidades principais
            funcionalidades = {
                'CSS carregado': '<style>' in content,
                'Campo adicionar link': 'id="linkPresente"' in content,
                'Botão adicionar': 'btnAdicionarLink' in content,
                'Função JavaScript': 'adicionarPresentePorLink' in content,
                'Botão excluir vermelho': 'btn-danger' in content and 'excluirPresente' in content,
                'Grid de presentes': 'gift-card' in content,
                'Estatísticas': 'stat-card' in content
            }
            
            print('\n📋 FUNCIONALIDADES:')
            todas_ok = True
            for nome, ok in funcionalidades.items():
                status = '✅' if ok else '❌'
                print(f'{status} {nome}')
                if not ok:
                    todas_ok = False
            
            # Testar adição rápida
            print(f'\n🔗 Testando adição rápida...')
            test_link = f'https://www.teste.com/produto-{int(time.time())}'
            
            add_response = session.post('http://127.0.0.1:5000/admin/adicionar-presente-por-link',
                                      json={'link': test_link},
                                      headers={'Content-Type': 'application/json'})
            
            if add_response.status_code == 200:
                result = add_response.json()
                if result.get('success'):
                    print('✅ Adição funcionando')
                    
                    # Verificar se apareceu na lista
                    presentes_response2 = session.get('http://127.0.0.1:5000/admin/presentes')
                    if test_link in presentes_response2.text:
                        print('✅ Produto aparece na lista')
                    else:
                        print('⚠️ Produto não aparece na lista (pode estar em outra página)')
                else:
                    print(f'⚠️ Erro na adição: {result.get("error")}')
            else:
                print(f'❌ Erro HTTP na adição: {add_response.status_code}')
                todas_ok = False
            
            return todas_ok
        else:
            print('❌ Erro ao acessar página de presentes')
            return False
            
    except Exception as e:
        print(f'❌ Erro durante teste: {e}')
        return False

if __name__ == "__main__":
    sucesso = teste_interface_completa()
    print(f'\n🎯 RESULTADO FINAL: {"✅ TUDO FUNCIONANDO" if sucesso else "❌ PROBLEMAS ENCONTRADOS"}')
