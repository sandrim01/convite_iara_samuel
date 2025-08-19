#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para popular presentes de exemplo
"""
from app import create_app, db
from app.models import Presente

# Criar aplicação
app = create_app()

with app.app_context():
    print("🎁 Populando presentes de exemplo...")
    
    # Verificar se já existem presentes
    if Presente.query.count() > 0:
        print(f"✅ Já existem {Presente.query.count()} presentes no banco.")
        resposta = input("Deseja adicionar mais presentes? (s/n): ")
        if resposta.lower() != 's':
            exit()
    
    # Lista de presentes para adicionar
    presentes_exemplo = [
        {
            'nome': 'Jogo de Panelas Antiaderente Tramontina',
            'descricao': 'Conjunto com 5 panelas antiaderentes de alumínio com revestimento interno e externo antiaderente. Inclui cabos ergonômicos e tampas de vidro temperado.',
            'categoria': 'cozinha',
            'preco_sugerido': 299.90,
            'link_loja': 'https://www.americanas.com.br/produto/1234567890',
            'imagem_url': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=500&h=400&fit=crop'
        },
        {
            'nome': 'Conjunto de Taças de Cristal Bohemia',
            'descricao': 'Kit com 6 taças de cristal para vinho tinto, branco e champanhe. Cristal tcheco de alta qualidade com design elegante.',
            'categoria': 'casa',
            'preco_sugerido': 189.90,
            'link_loja': 'https://www.magazineluiza.com.br/produto/987654321',
            'imagem_url': 'https://images.unsplash.com/photo-1546171753-97d7676e4602?w=500&h=400&fit=crop'
        },
        {
            'nome': 'Jogo de Cama King Size Premium',
            'descricao': 'Jogo de cama 100% algodão percal 200 fios, 4 peças, king size. Inclui lençol de elástico, lençol de cima e 2 fronhas.',
            'categoria': 'quarto',
            'preco_sugerido': 159.90,
            'link_loja': 'https://www.casasbahia.com.br/produto/456789123',
            'imagem_url': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=500&h=400&fit=crop'
        },
        {
            'nome': 'Cafeteira Elétrica Philco PCF41',
            'descricao': 'Cafeteira elétrica programável para até 30 xícaras, com timer digital, filtro permanente lavável e sistema corta-pingos.',
            'categoria': 'cozinha',
            'preco_sugerido': 149.90,
            'link_loja': 'https://www.extra.com.br/produto/789123456',
            'imagem_url': 'https://images.unsplash.com/photo-1495774856032-8b90bbb32b32?w=500&h=400&fit=crop'
        },
        {
            'nome': 'Conjunto de Almofadas Decorativas',
            'descricao': 'Kit com 4 almofadas decorativas para sala de estar, com capas em tecido suede nas cores neutras. Medidas: 45x45cm.',
            'categoria': 'sala',
            'preco_sugerido': 79.90,
            'link_loja': 'https://www.pontofrio.com.br/produto/321654987',
            'imagem_url': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=500&h=400&fit=crop'
        },
        {
            'nome': 'Aspirador de Pó Robô Smart',
            'descricao': 'Aspirador de pó robô inteligente com mapeamento, controle por aplicativo, bateria de longa duração e estação de recarga automática.',
            'categoria': 'eletronicos',
            'preco_sugerido': 899.90,
            'link_loja': 'https://www.submarino.com.br/produto/654987321',
            'imagem_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=500&h=400&fit=crop'
        },
        {
            'nome': 'Spa Day para Dois',
            'descricao': 'Voucher para day spa completo para o casal, incluindo massagem relaxante, tratamento facial, acesso à sauna e piscina aquecida.',
            'categoria': 'experiencias',
            'preco_sugerido': 450.00,
            'link_loja': 'https://www.spa-exemplo.com.br/voucher',
            'imagem_url': 'https://images.unsplash.com/photo-1540555700478-4be289fbecef?w=500&h=400&fit=crop'
        },
        {
            'nome': 'Aparelho de Jantar 20 Peças Oxford',
            'descricao': 'Aparelho de jantar em porcelana branca com filete dourado, 20 peças para 4 pessoas. Inclui pratos rasos, fundos, sobremesa, xícaras e pires.',
            'categoria': 'casa',
            'preco_sugerido': 199.90,
            'link_loja': 'https://www.ricardo-eletro.com.br/produto/147258369',
            'imagem_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=500&h=400&fit=crop'
        },
        {
            'nome': 'Liquidificador Vitamix High Power',
            'descricao': 'Liquidificador profissional de alta potência com 12 velocidades, lâminas de aço inox e copo de 2 litros livre de BPA.',
            'categoria': 'cozinha',
            'preco_sugerido': 379.90,
            'link_loja': 'https://www.fastshop.com.br/produto/258369147',
            'imagem_url': 'https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=500&h=400&fit=crop'
        },
        {
            'nome': 'Kit Toalhas de Banho Premium',
            'descricao': 'Conjunto com 4 toalhas de banho 100% algodão fio penteado, super absorventes e macias. Cores neutras elegantes.',
            'categoria': 'banheiro',
            'preco_sugerido': 129.90,
            'link_loja': 'https://www.leroy.com.br/produto/369147258',
            'imagem_url': 'https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=500&h=400&fit=crop'
        }
    ]
    
    # Adicionar presentes
    presentes_adicionados = 0
    for presente_data in presentes_exemplo:
        # Verificar se já existe
        existe = Presente.query.filter_by(nome=presente_data['nome']).first()
        if not existe:
            presente = Presente(**presente_data)
            db.session.add(presente)
            presentes_adicionados += 1
            print(f"  ✅ {presente_data['nome']}")
        else:
            print(f"  ⚠️ {presente_data['nome']} (já existe)")
    
    # Commit das mudanças
    if presentes_adicionados > 0:
        db.session.commit()
        print(f"\n🎉 {presentes_adicionados} presentes adicionados com sucesso!")
    else:
        print("\n✅ Todos os presentes já existem no banco.")
    
    print(f"\n📊 Total de presentes no banco: {Presente.query.count()}")
    print("🎁 População de presentes concluída!")
