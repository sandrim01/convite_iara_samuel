#!/usr/bin/env python3
"""
Diagnóstico completo do sistema de presentes
"""

from app import create_app, db
from app.models import Presente, EscolhaPresente
from sqlalchemy import inspect
import traceback

def diagnosticar_presentes():
    print("🔍 DIAGNÓSTICO COMPLETO DO SISTEMA DE PRESENTES")
    print("=" * 60)
    
    app = create_app()
    with app.app_context():
        try:
            # 1. Verificar tabelas
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print("1. VERIFICAÇÃO DE TABELAS:")
            print(f"   📋 Tabelas disponíveis: {tables}")
            
            tabelas_necessarias = ['presente', 'escolha_presente']
            for tabela in tabelas_necessarias:
                if tabela in tables:
                    print(f"   ✅ Tabela '{tabela}' existe")
                    
                    # Mostrar campos
                    columns = [c['name'] for c in inspector.get_columns(tabela)]
                    print(f"      Campos: {columns}")
                else:
                    print(f"   ❌ Tabela '{tabela}' NÃO existe!")
            
            # 2. Verificar modelo Presente
            print("\n2. VERIFICAÇÃO DO MODELO PRESENTE:")
            try:
                total_presentes = Presente.query.count()
                print(f"   📊 Total de presentes: {total_presentes}")
                
                if total_presentes > 0:
                    presentes = Presente.query.limit(3).all()
                    print("   📝 Exemplos de presentes:")
                    for p in presentes:
                        print(f"      - ID: {p.id}, Nome: {p.nome}, Preço: R$ {p.preco_sugerido:.2f}")
                        print(f"        Categoria: {p.categoria}, Disponível: {p.disponivel}")
                else:
                    print("   ⚠️ Nenhum presente no banco de dados")
                    
            except Exception as e:
                print(f"   ❌ Erro ao consultar presentes: {e}")
                traceback.print_exc()
            
            # 3. Verificar modelo EscolhaPresente
            print("\n3. VERIFICAÇÃO DE ESCOLHAS:")
            try:
                total_escolhas = EscolhaPresente.query.count()
                print(f"   📊 Total de escolhas: {total_escolhas}")
                
                if total_escolhas > 0:
                    escolhas = EscolhaPresente.query.limit(3).all()
                    print("   📝 Exemplos de escolhas:")
                    for e in escolhas:
                        print(f"      - Presente ID: {e.presente_id}, Convidado: {e.nome_convidado}")
                        print(f"        Email: {e.email_convidado}, Data: {e.data_escolha}")
                        
            except Exception as e:
                print(f"   ❌ Erro ao consultar escolhas: {e}")
                traceback.print_exc()
            
            # 4. Testar criação de presente
            print("\n4. TESTE DE CRIAÇÃO DE PRESENTE:")
            try:
                # Criar um presente de teste
                teste_presente = Presente(
                    nome="Teste - Jogo de Pratos",
                    descricao="Presente de teste para diagnóstico",
                    preco_sugerido=150.00,
                    categoria="Mesa e Cozinha",
                    link_loja="https://exemplo.com",
                    disponivel=True
                )
                
                db.session.add(teste_presente)
                db.session.commit()
                
                print("   ✅ Presente de teste criado com sucesso!")
                print(f"      ID: {teste_presente.id}")
                
                # Remover o presente de teste
                db.session.delete(teste_presente)
                db.session.commit()
                print("   🧹 Presente de teste removido")
                
            except Exception as e:
                print(f"   ❌ Erro ao criar presente de teste: {e}")
                traceback.print_exc()
                db.session.rollback()
            
            print("\n" + "=" * 60)
            print("RESULTADO DO DIAGNÓSTICO:")
            
            if 'presente' not in tables:
                print("❌ PROBLEMA: Tabela 'presente' não existe!")
                print("💡 SOLUÇÃO: Criar as tabelas com db.create_all()")
            elif total_presentes == 0:
                print("⚠️ AVISO: Tabelas existem mas não há presentes cadastrados")
                print("💡 SOLUÇÃO: Adicionar presentes via admin ou popular com dados")
            else:
                print("✅ Sistema de presentes funcionando corretamente!")
                
        except Exception as e:
            print(f"❌ ERRO GERAL: {e}")
            traceback.print_exc()

if __name__ == "__main__":
    diagnosticar_presentes()
