#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste simples das funcionalidades de presentes com login
"""
from app import create_app
from app.models import Presente, Admin, db

app = create_app()

with app.test_client() as client:
    print("🧪 Testando funcionalidades de presentes (com login)...")
    
    # Primeiro fazer login
    print("\n🔑 Fazendo login...")
    login_data = {
        'username': 'admin',
        'password': 'admin'
    }
    
    response = client.post('/admin/login', data=login_data, follow_redirects=False)
    print(f"Status login: {response.status_code}")
    
    if response.status_code == 302:
        print("✅ Login realizado com sucesso!")
        
        # Agora testar as páginas de presentes
        print("\n1️⃣ Testando listagem de presentes...")
        response = client.get('/admin/presentes')
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Página de listagem carregou com sucesso!")
            # Verificar se tem presentes listados
            content = response.data.decode('utf-8')
            if 'presente-card' in content:
                print("✅ Presentes sendo exibidos na página!")
            else:
                print("⚠️ Nenhum presente visível na página")
        else:
            print("❌ Erro ao carregar página de listagem")
        
        print("\n2️⃣ Testando página de adicionar presente...")
        response = client.get('/admin/presentes/adicionar')
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Página de adicionar presente carregou com sucesso!")
            # Verificar se o formulário está presente
            content = response.data.decode('utf-8')
            if 'name="nome"' in content and 'name="categoria"' in content:
                print("✅ Formulário de adição presente na página!")
            else:
                print("⚠️ Formulário pode estar incompleto")
        else:
            print("❌ Erro ao carregar página de adicionar")
        
        print("\n3️⃣ Testando adição de presente...")
        dados_presente = {
            'nome': 'Teste API Present',
            'descricao': 'Presente adicionado via teste',
            'categoria': 'diversos',
            'preco_sugerido': '75.50',
        }
        
        response = client.post('/admin/presentes/adicionar', 
                              data=dados_presente, 
                              follow_redirects=False)
        print(f"Status: {response.status_code}")
        if response.status_code == 302:
            print("✅ Presente adicionado com sucesso!")
            
            # Verificar no banco
            with app.app_context():
                presente_teste = Presente.query.filter_by(nome='Teste API Present').first()
                if presente_teste:
                    print(f"✅ Presente confirmado no banco! ID: {presente_teste.id}")
                    
                    # Testar edição
                    print(f"\n4️⃣ Testando edição do presente ID {presente_teste.id}...")
                    response = client.get(f'/admin/presentes/{presente_teste.id}/editar')
                    if response.status_code == 200:
                        print("✅ Página de edição carregou!")
                        
                        # Editar o presente
                        dados_editados = {
                            'nome': 'Teste API Present EDITADO',
                            'descricao': 'Presente editado via teste',
                            'categoria': 'casa',
                            'preco_sugerido': '99.99'
                        }
                        
                        response = client.post(f'/admin/presentes/{presente_teste.id}/editar',
                                             data=dados_editados,
                                             follow_redirects=False)
                        if response.status_code == 302:
                            print("✅ Presente editado com sucesso!")
                        else:
                            print(f"❌ Erro ao editar: {response.status_code}")
                    else:
                        print(f"❌ Erro ao carregar página de edição: {response.status_code}")
                    
                    # Testar remoção
                    print(f"\n5️⃣ Testando remoção do presente ID {presente_teste.id}...")
                    response = client.post(f'/admin/presentes/{presente_teste.id}/remover',
                                         follow_redirects=False)
                    if response.status_code == 302:
                        print("✅ Presente removido com sucesso!")
                        
                        # Verificar se foi removido do banco
                        presente_removido = Presente.query.get(presente_teste.id)
                        if not presente_removido:
                            print("✅ Remoção confirmada no banco!")
                        else:
                            print("❌ Presente ainda existe no banco")
                    else:
                        print(f"❌ Erro ao remover: {response.status_code}")
                else:
                    print("❌ Presente não encontrado no banco")
        else:
            print(f"❌ Erro ao adicionar presente: {response.status_code}")
    else:
        print("❌ Falha no login")
        print(f"Conteúdo: {response.data.decode('utf-8')[:300]}")
    
    # Estatísticas finais
    print("\n📊 Estatísticas finais:")
    with app.app_context():
        total_presentes = Presente.query.count()
        print(f"   Total de presentes: {total_presentes}")
    
    print("\n🎉 Teste concluído!")
