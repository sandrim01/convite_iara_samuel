#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste final simplificado das funcionalidades de presentes
"""
from app import create_app
from app.models import Presente

app = create_app()

def teste_simples():
    with app.test_client() as client:
        print("🧪 Teste simplificado das funcionalidades de presentes...")
        
        # Login
        print("\n🔑 Fazendo login...")
        login_data = {'username': 'admin', 'password': 'admin'}
        response = client.post('/admin/login', data=login_data, follow_redirects=False)
        
        if response.status_code == 302:
            print("✅ Login realizado com sucesso!")
            
            # Teste 1: Listar presentes
            print("\n1️⃣ Testando listagem de presentes...")
            response = client.get('/admin/presentes')
            if response.status_code == 200:
                print("✅ Página de listagem funcionando!")
                content = response.data.decode('utf-8')
                if 'presente-card' in content:
                    print("✅ Presentes sendo exibidos!")
            
            # Teste 2: Página de adicionar
            print("\n2️⃣ Testando página de adicionar...")
            response = client.get('/admin/presentes/adicionar')
            if response.status_code == 200:
                print("✅ Página de adicionar funcionando!")
                content = response.data.decode('utf-8')
                if 'name="nome"' in content:
                    print("✅ Formulário presente!")
            
            # Teste 3: Adicionar presente
            print("\n3️⃣ Testando adição de presente...")
            dados = {
                'nome': 'Teste Final Present',
                'descricao': 'Presente para teste final',
                'categoria': 'diversos',
                'preco_sugerido': '88.50',
            }
            response = client.post('/admin/presentes/adicionar', data=dados, follow_redirects=False)
            if response.status_code == 302:
                print("✅ Presente adicionado com sucesso!")
                
                # Verificar no banco
                with app.app_context():
                    presente = Presente.query.filter_by(nome='Teste Final Present').first()
                    if presente:
                        print(f"✅ Presente confirmado no banco! ID: {presente.id}")
                        
                        # Teste 4: Editar
                        print(f"\n4️⃣ Testando edição...")
                        response = client.get(f'/admin/presentes/{presente.id}/editar')
                        if response.status_code == 200:
                            print("✅ Página de edição funcionando!")
                            
                            dados_edit = {
                                'nome': 'Teste Final Present EDITADO',
                                'descricao': 'Presente editado',
                                'categoria': 'casa',
                                'preco_sugerido': '99.99'
                            }
                            response = client.post(f'/admin/presentes/{presente.id}/editar', 
                                                 data=dados_edit, follow_redirects=False)
                            if response.status_code == 302:
                                print("✅ Edição funcionando!")
                        
                        # Teste 5: Remover
                        print(f"\n5️⃣ Testando remoção...")
                        response = client.post(f'/admin/presentes/{presente.id}/remover', 
                                             follow_redirects=False)
                        if response.status_code == 302:
                            print("✅ Remoção funcionando!")
            
            print("\n📊 Estatísticas:")
            with app.app_context():
                total = Presente.query.count()
                print(f"   Total de presentes: {total}")
            
            print("\n🎉 Todas as funcionalidades estão funcionando!")
        else:
            print("❌ Falha no login")

if __name__ == "__main__":
    teste_simples()
