#!/usr/bin/env python3
"""
Teste simples para verificar se a rota do convite de recepção está funcionando
"""

import requests
import sys
from flask import Flask
from app import create_app
import time

def teste_rota_convite():
    """Testa a rota /convite-recepcao"""
    
    print("🧪 Testando rota do convite de recepção...")
    
    try:
        # Teste direto com Flask
        app = create_app()
        
        with app.test_client() as client:
            print("📡 Fazendo requisição para /convite-recepcao...")
            response = client.get('/convite-recepcao')
            
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Sucesso! O convite de recepção está funcionando!")
                print(f"📄 Tamanho da resposta: {len(response.data)} bytes")
                
                # Verifica se o HTML contém elementos esperados
                html_content = response.data.decode('utf-8')
                if 'Recepção' in html_content:
                    print("✅ Conteúdo da recepção encontrado no HTML")
                else:
                    print("⚠️  Conteúdo da recepção não encontrado")
                    
                return True
                
            elif response.status_code == 500:
                print("❌ Erro 500 - Erro interno do servidor")
                print(f"🔍 Response data: {response.data.decode('utf-8')[:500]}...")
                return False
                
            else:
                print(f"⚠️  Status code inesperado: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Erro durante o teste: {str(e)}")
        return False

def teste_template_direto():
    """Testa o template diretamente"""
    
    print("\n🎭 Testando template diretamente...")
    
    try:
        from flask import Flask, render_template
        from app import create_app
        
        app = create_app()
        
        with app.app_context():
            try:
                html = render_template('convite_recepcao.html')
                print("✅ Template renderizado com sucesso!")
                print(f"📄 Tamanho do HTML: {len(html)} caracteres")
                return True
            except Exception as e:
                print(f"❌ Erro ao renderizar template: {str(e)}")
                return False
                
    except Exception as e:
        print(f"❌ Erro ao testar template: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando testes do convite de recepção...\n")
    
    # Teste 1: Template direto
    template_ok = teste_template_direto()
    
    # Teste 2: Rota completa
    rota_ok = teste_rota_convite()
    
    print("\n📋 Resumo dos testes:")
    print(f"   Template: {'✅ OK' if template_ok else '❌ ERRO'}")
    print(f"   Rota: {'✅ OK' if rota_ok else '❌ ERRO'}")
    
    if template_ok and rota_ok:
        print("\n🎉 Todos os testes passaram! O convite de recepção está funcionando.")
        sys.exit(0)
    else:
        print("\n⚠️  Alguns testes falharam. Verifique os erros acima.")
        sys.exit(1)
