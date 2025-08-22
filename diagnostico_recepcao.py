#!/usr/bin/env python3
"""
Diagnóstico completo do convite de recepção
"""

def teste_importacao():
    """Testa se a aplicação pode ser importada"""
    print("🔍 Testando importação da aplicação...")
    try:
        from app import create_app
        app = create_app()
        print("✅ Aplicação importada com sucesso")
        return app
    except Exception as e:
        print(f"❌ Erro ao importar aplicação: {e}")
        return None

def teste_template_direto(app):
    """Testa se o template pode ser renderizado"""
    print("\n🎭 Testando renderização do template...")
    try:
        with app.app_context():
            from flask import render_template
            html = render_template('convite_recepcao.html')
            print(f"✅ Template renderizado com sucesso ({len(html)} caracteres)")
            return True
    except Exception as e:
        print(f"❌ Erro ao renderizar template: {e}")
        return False

def teste_rota_direta(app):
    """Testa a rota usando test_client"""
    print("\n📡 Testando rota com test_client...")
    try:
        with app.test_client() as client:
            response = client.get('/convite-recepcao')
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print(f"✅ Rota funcionando ({len(response.data)} bytes)")
                return True
            else:
                print(f"❌ Erro na rota: {response.status_code}")
                if response.data:
                    print(f"Dados: {response.data.decode('utf-8')[:500]}...")
                return False
    except Exception as e:
        print(f"❌ Erro ao testar rota: {e}")
        return False

def verificar_arquivos():
    """Verifica se os arquivos necessários existem"""
    print("\n📁 Verificando arquivos...")
    import os
    
    arquivos = [
        'app/templates/convite_recepcao.html',
        'app/routes/convite.py',
        'app/models.py'
    ]
    
    for arquivo in arquivos:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo} existe")
        else:
            print(f"❌ {arquivo} NÃO EXISTE")

def main():
    print("🚀 Diagnóstico completo do convite de recepção\n")
    
    # Teste 1: Verificar arquivos
    verificar_arquivos()
    
    # Teste 2: Importação
    app = teste_importacao()
    if not app:
        print("\n❌ Falha crítica: não foi possível importar a aplicação")
        return
    
    # Teste 3: Template
    template_ok = teste_template_direto(app)
    
    # Teste 4: Rota
    rota_ok = teste_rota_direta(app)
    
    print("\n" + "="*50)
    print("📋 RESUMO DO DIAGNÓSTICO:")
    print(f"   Importação: ✅ OK")
    print(f"   Template: {'✅ OK' if template_ok else '❌ ERRO'}")
    print(f"   Rota: {'✅ OK' if rota_ok else '❌ ERRO'}")
    
    if template_ok and rota_ok:
        print("\n🎉 TUDO FUNCIONANDO! O problema pode ser de conectividade.")
    else:
        print("\n⚠️ PROBLEMAS DETECTADOS. Verifique os erros acima.")

if __name__ == "__main__":
    main()
