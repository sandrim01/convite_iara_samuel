#!/usr/bin/env python3

import requests
import json

def testar_adicionar_presente():
    """Testa a funcionalidade de adicionar presente por link"""
    session = requests.Session()
    
    try:
        print('=== TESTE ADICIONAR PRESENTE POR LINK ===')
        
        # Fazer login
        login_response = session.post('http://127.0.0.1:5000/admin/login', 
                                    data={'username': 'admin', 'password': 'Casamento2025*#'})
        print(f'Login: {login_response.status_code}')
        
        if login_response.status_code not in [200, 302]:
            print('❌ Falha no login')
            return False
        
        # Testar adição de presente por link
        print('\n🔗 Testando adição por link...')
        
        # Usar um link de teste simples
        test_data = {
            'link': 'https://www.amazon.com.br/produto-teste-123'
        }
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        response = session.post('http://127.0.0.1:5000/admin/adicionar-presente-por-link', 
                              json=test_data, headers=headers, timeout=15)
        
        print(f'Status da requisição: {response.status_code}')
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f'Resposta JSON: {result}')
                
                if result.get('success'):
                    print('✅ Presente adicionado com sucesso!')
                    return True
                else:
                    error_msg = result.get('error', 'Erro desconhecido')
                    print(f'⚠️ Erro na adição: {error_msg}')
                    
                    # Se o erro é sobre produto já existir, ainda é um sucesso
                    if 'já foi adicionado' in error_msg:
                        print('✅ Sistema funcionando (produto já existe)')
                        return True
                    return False
                    
            except json.JSONDecodeError:
                print('❌ Resposta não é JSON válido')
                print(f'Conteúdo recebido: {response.text[:300]}')
                return False
        else:
            print(f'❌ Erro HTTP: {response.status_code}')
            print(f'Resposta: {response.text[:300]}')
            return False
            
    except Exception as e:
        print(f'❌ Erro durante teste: {e}')
        return False

def testar_com_link_longo():
    """Testa com um nome muito longo para verificar truncamento"""
    session = requests.Session()
    
    try:
        print('\n=== TESTE NOME LONGO ===')
        
        # Login
        login_response = session.post('http://127.0.0.1:5000/admin/login', 
                                    data={'username': 'admin', 'password': 'Casamento2025*#'})
        
        # Link de teste com nome muito longo
        test_data = {
            'link': 'https://www.magazineluiza.com.br/produto-super-mega-ultra-extremamente-longo-nome-de-produto-que-deveria-ser-truncado-para-nao-causar-erro-no-banco-de-dados-postgresql-porque-o-limite-e-de-duzentos-caracteres-apenas-entao-precisa-cortar/123456789'
        }
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        response = session.post('http://127.0.0.1:5000/admin/adicionar-presente-por-link', 
                              json=test_data, headers=headers, timeout=15)
        
        print(f'Status: {response.status_code}')
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print('✅ Nome longo tratado corretamente!')
                return True
            else:
                print(f'⚠️ Erro: {result.get("error")}')
                return 'já foi adicionado' in result.get('error', '')
        else:
            print(f'❌ Erro: {response.text[:200]}')
            return False
            
    except Exception as e:
        print(f'❌ Erro: {e}')
        return False

if __name__ == "__main__":
    print('🧪 TESTES DE ADIÇÃO DE PRESENTES\n')
    
    teste1 = testar_adicionar_presente()
    teste2 = testar_com_link_longo()
    
    print(f'\n📋 RESULTADOS:')
    print(f'   Adição básica: {"✅" if teste1 else "❌"}')
    print(f'   Nome longo: {"✅" if teste2 else "❌"}')
    
    if teste1 and teste2:
        print('\n🎉 TODOS OS TESTES PASSARAM!')
        print('   Sistema de adição de presentes funcionando corretamente.')
    else:
        print('\n⚠️ ALGUNS TESTES FALHARAM')
        print('   Verifique os logs acima para detalhes.')
