#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste das funcionalidades de presentes no admin
"""
from app import create_app
from app.models import Presente, db

app = create_app()

with app.test_client() as client:
    print("🧪 Testando funcionalidades de presentes...")
    
    # Teste 1: Acessar página de listagem de presentes
    print("\n1️⃣ Testando listagem de presentes...")
    response = client.get('/admin/presentes')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Página de listagem carregou com sucesso!")
    else:
        print("❌ Erro ao carregar página de listagem")
        print(f"Conteúdo: {response.data.decode('utf-8')[:500]}")
    
    # Teste 2: Acessar página de adicionar presente
    print("\n2️⃣ Testando página de adicionar presente...")
    response = client.get('/admin/adicionar_presente')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Página de adicionar presente carregou com sucesso!")
    else:
        print("❌ Erro ao carregar página de adicionar")
        print(f"Conteúdo: {response.data.decode('utf-8')[:500]}")
    
    # Teste 3: Adicionar um presente via POST
    print("\n3️⃣ Testando adição de presente...")
    dados_presente = {
        'nome': 'Presente de Teste',
        'descricao': 'Descrição do presente de teste',
        'categoria': 'diversos',
        'preco_sugerido': '99.99',
        'link_loja': 'https://teste.com',
        'imagem_url': 'https://exemplo.com/imagem.jpg'
    }
    
    response = client.post('/admin/processar_adicionar_presente', 
                          data=dados_presente, 
                          follow_redirects=False)
    print(f"Status: {response.status_code}")
    if response.status_code == 302:
        print("✅ Presente adicionado com sucesso! (Redirecionamento)")
        redirect_location = response.headers.get('Location', '')
        print(f"Redirecionando para: {redirect_location}")
    else:
        print("❌ Erro ao adicionar presente")
        print(f"Conteúdo: {response.data.decode('utf-8')[:500]}")
    
    # Teste 4: Verificar se o presente foi adicionado no banco
    print("\n4️⃣ Verificando no banco de dados...")
    with app.app_context():
        presente_teste = Presente.query.filter_by(nome='Presente de Teste').first()
        if presente_teste:
            print("✅ Presente encontrado no banco!")
            print(f"   ID: {presente_teste.id}")
            print(f"   Nome: {presente_teste.nome}")
            print(f"   Categoria: {presente_teste.categoria}")
            print(f"   Preço: R$ {presente_teste.preco_sugerido}")
            
            # Teste 5: Editar o presente
            print("\n5️⃣ Testando edição de presente...")
            response = client.get(f'/admin/presentes/{presente_teste.id}/editar')
            print(f"Status página edição: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Página de edição carregou com sucesso!")
                
                # Editar o presente
                dados_editados = {
                    'nome': 'Presente de Teste EDITADO',
                    'descricao': 'Descrição editada',
                    'categoria': 'casa',
                    'preco_sugerido': '149.99'
                }
                
                response = client.post(f'/admin/presentes/{presente_teste.id}/editar',
                                     data=dados_editados,
                                     follow_redirects=False)
                print(f"Status edição: {response.status_code}")
                
                if response.status_code == 302:
                    print("✅ Presente editado com sucesso!")
                    
                    # Verificar edição no banco
                    presente_editado = Presente.query.get(presente_teste.id)
                    if presente_editado.nome == 'Presente de Teste EDITADO':
                        print("✅ Edição confirmada no banco!")
                    else:
                        print("❌ Edição não aplicada no banco")
                else:
                    print("❌ Erro ao editar presente")
            
            # Teste 6: Remover o presente
            print("\n6️⃣ Testando remoção de presente...")
            response = client.post(f'/admin/presentes/{presente_teste.id}/remover',
                                 follow_redirects=False)
            print(f"Status remoção: {response.status_code}")
            
            if response.status_code == 302:
                print("✅ Presente removido com sucesso!")
                
                # Verificar remoção no banco
                presente_removido = Presente.query.get(presente_teste.id)
                if not presente_removido:
                    print("✅ Remoção confirmada no banco!")
                else:
                    print("❌ Presente ainda existe no banco")
            else:
                print("❌ Erro ao remover presente")
        else:
            print("❌ Presente não foi encontrado no banco")
    
    # Teste 7: Estatísticas finais
    print("\n7️⃣ Estatísticas finais...")
    with app.app_context():
        total_presentes = Presente.query.count()
        print(f"📊 Total de presentes no banco: {total_presentes}")
        
        # Presentes por categoria
        categorias = db.session.query(Presente.categoria, db.func.count(Presente.id)).group_by(Presente.categoria).all()
        print("📋 Presentes por categoria:")
        for categoria, count in categorias:
            print(f"   {categoria}: {count}")
    
    print("\n🎉 Teste de funcionalidades de presentes concluído!")
