import requests
import re

def teste_rapido():
    session = requests.Session()
    
    # Login
    login_data = {'username': 'master', 'password': 'master123'}
    login_response = session.post('http://localhost:5000/admin/login', data=login_data)
    print('Login Status:', 'SUCCESS' if 'dashboard' in login_response.url else 'FAILED')
    
    # Verificar presentes
    presentes_response = session.get('http://localhost:5000/admin/presentes')
    print('Presentes Page Status:', presentes_response.status_code)
    
    # Procurar IDs
    ids = re.findall(r"onclick=\"confirmarRemocao\('(\d+)'", presentes_response.text)
    print('IDs encontrados:', ids[:3])
    
    if ids:
        # Testar remoção do primeiro
        primeiro_id = ids[0]
        print(f'Tentando remover ID: {primeiro_id}')
        remove_response = session.post(f'http://localhost:5000/admin/presentes/{primeiro_id}/remover')
        print('Remove Status:', remove_response.status_code)
        print('Final URL:', remove_response.url)
        
        if remove_response.status_code == 200:
            print('✅ API FUNCIONANDO - O problema é no JavaScript do navegador')
        else:
            print('❌ API com problema')
    else:
        print('❌ Nenhum presente encontrado')

if __name__ == "__main__":
    teste_rapido()
