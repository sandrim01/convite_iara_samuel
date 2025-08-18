#!/usr/bin/env python3
"""
Sistema de Convite de Casamento - Popular Presentes
Iara & Samuel
"""

import os
import sys

# Adicionar o diretório do projeto ao path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app import create_app
from app.extensions import db
from app.models import Presente

def popular_presentes():
    """Popula o banco de dados com presentes para casamento"""
    
    app = create_app()
    
    with app.app_context():
        # Lista de presentes com imagens e detalhes realistas
        presentes_data = [
            # Cozinha
            {
                "nome": "Jogo de Panelas Tramontina 5 Peças",
                "descricao": "Conjunto completo de panelas antiaderentes com cabos de baquelite - Loja: Magazine Luiza",
                "categoria": "cozinha",
                "preco_sugerido": 299.90,
                "link_loja": "https://www.magazineluiza.com.br",
                "imagem_url": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=500&h=500&fit=crop"
            },
            {
                "nome": "Micro-ondas Electrolux 20L",
                "descricao": "Micro-ondas com 10 níveis de potência e função descongelar - Loja: Casas Bahia",
                "categoria": "cozinha",
                "preco_sugerido": 459.00,
                "link_loja": "https://www.casasbahia.com.br",
                "imagem_url": "https://images.unsplash.com/photo-1574269909862-7e1d70bb8078?w=500&h=500&fit=crop"
            },
            {
                "nome": "Liquidificador Philips Walita",
                "descricao": "Liquidificador de alta potência com jarra de vidro de 2 litros - Loja: Extra",
                "categoria": "cozinha",
                "preco_sugerido": 189.90,
                "link_loja": "https://www.extra.com.br",
                "imagem_url": "https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=500&h=500&fit=crop"
            },
            {
                "nome": "Jogo de Pratos 18 Peças",
                "descricao": "Aparelho de jantar em porcelana branca com detalhes dourados - Loja: Tok&Stok",
                "categoria": "cozinha",
                "preco_sugerido": 159.90,
                "link_loja": "https://www.tokstok.com.br",
                "imagem_url": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=500&h=500&fit=crop"
            },
            {
                "nome": "Cafeteira Elétrica Mondial",
                "descricao": "Cafeteira para 30 xícaras com jarra de vidro e filtro permanente - Loja: Submarino",
                "categoria": "cozinha",
                "preco_sugerido": 89.90,
                "link_loja": "https://www.submarino.com.br",
                "imagem_url": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=500&h=500&fit=crop"
            },
            
            # Quarto
            {
                "nome": "Jogo de Cama Casal 180 Fios",
                "descricao": "Jogo de lençol casal king com fronhas em algodão 180 fios - Loja: Lojas Americanas",
                "categoria": "quarto",
                "preco_sugerido": 119.90,
                "link_loja": "https://www.americanas.com.br",
                "imagem_url": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=500&h=500&fit=crop"
            },
            {
                "nome": "Travesseiro Viscoelástico",
                "descricao": "Par de travesseiros anatômicos em viscoelástico - Loja: Casas Bahia",
                "categoria": "quarto",
                "preco_sugerido": 159.90,
                "link_loja": "https://www.casasbahia.com.br",
                "imagem_url": "https://images.unsplash.com/photo-1586998704331-915b1f31429a?w=500&h=500&fit=crop"
            },
            {
                "nome": "Edredom Casal Dupla Face",
                "descricao": "Edredom casal king dupla face em microfibra - Loja: Magazine Luiza",
                "categoria": "quarto",
                "preco_sugerido": 89.90,
                "link_loja": "https://www.magazineluiza.com.br",
                "imagem_url": "https://images.unsplash.com/photo-1586997003405-7e49c22678db?w=500&h=500&fit=crop"
            },
            
            # Sala
            {
                "nome": "Tapete Decorativo 2x1,5m",
                "descricao": "Tapete felpudo para sala com estampa geométrica moderna - Loja: Tok&Stok",
                "categoria": "sala",
                "preco_sugerido": 199.90,
                "link_loja": "https://www.tokstok.com.br",
                "imagem_url": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=500&h=500&fit=crop"
            },
            {
                "nome": "Almofadas Decorativas Kit 4un",
                "descricao": "Kit com 4 almofadas decorativas em tons neutros - Loja: Leroy Merlin",
                "categoria": "sala",
                "preco_sugerido": 79.90,
                "link_loja": "https://www.leroymerlin.com.br",
                "imagem_url": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=500&h=500&fit=crop"
            },
            {
                "nome": "Luminária de Mesa Moderna",
                "descricao": "Abajur de mesa com cúpula em tecido e base em madeira - Loja: Etna",
                "categoria": "sala",
                "preco_sugerido": 149.90,
                "link_loja": "https://www.etna.com.br",
                "imagem_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500&h=500&fit=crop"
            },
            
            # Casa
            {
                "nome": "Aspirador de Pó Electrolux",
                "descricao": "Aspirador de pó com filtro HEPA e acessórios completos - Loja: Fast Shop",
                "categoria": "casa",
                "preco_sugerido": 299.90,
                "link_loja": "https://www.fastshop.com.br",
                "imagem_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=500&h=500&fit=crop"
            },
            {
                "nome": "Ferro de Passar Philips",
                "descricao": "Ferro a vapor com base antiaderente e controle de temperatura - Loja: Ponto Frio",
                "categoria": "casa",
                "preco_sugerido": 89.90,
                "link_loja": "https://www.pontofrio.com.br",
                "imagem_url": "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=500&h=500&fit=crop"
            },
            {
                "nome": "Conjunto de Toalhas 5 Peças",
                "descricao": "Kit de toalhas de banho e rosto em algodão 100% - Loja: Renner",
                "categoria": "casa",
                "preco_sugerido": 69.90,
                "link_loja": "https://www.lojasrenner.com.br",
                "imagem_url": "https://images.unsplash.com/photo-1586999768726-a824aa3bbb82?w=500&h=500&fit=crop"
            },
            
            # Experiências
            {
                "nome": "Jantar Romântico para Dois",
                "descricao": "Vale para jantar romântico em restaurante especial - Voucher Experiência",
                "categoria": "experiencias",
                "preco_sugerido": 200.00,
                "link_loja": "",
                "imagem_url": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=500&h=500&fit=crop"
            },
            {
                "nome": "Fim de Semana em Pousada",
                "descricao": "Voucher para fim de semana romântico em pousada na região - Booking",
                "categoria": "experiencias",
                "preco_sugerido": 500.00,
                "link_loja": "https://www.booking.com",
                "imagem_url": "https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=500&h=500&fit=crop"
            },
            {
                "nome": "Sessão de Massagem para Casal",
                "descricao": "Voucher para spa day com massagem relaxante para dois - Spa Local",
                "categoria": "experiencias",
                "preco_sugerido": 300.00,
                "link_loja": "",
                "imagem_url": "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?w=500&h=500&fit=crop"
            }
        ]
        
        # Limpar tabela existente
        print("🗑️ Limpando presentes existentes...")
        Presente.query.delete()
        
        # Adicionar novos presentes
        print("🎁 Adicionando novos presentes...")
        for presente_data in presentes_data:
            presente = Presente(**presente_data)
            db.session.add(presente)
        
        # Salvar no banco
        db.session.commit()
        print(f"✅ {len(presentes_data)} presentes adicionados com sucesso!")
        
        # Mostrar estatísticas
        total = Presente.query.count()
        por_categoria = db.session.query(Presente.categoria, db.func.count(Presente.id)).group_by(Presente.categoria).all()
        
        print(f"📊 Total de presentes: {total}")
        print("📈 Por categoria:")
        for categoria, count in por_categoria:
            print(f"   {categoria}: {count}")

if __name__ == "__main__":
    popular_presentes()
