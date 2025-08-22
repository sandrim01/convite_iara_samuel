#!/usr/bin/env python3
"""
Teste específico para identificar o problema do url_for
"""

def teste_template_com_contexto():
    """Testa o template com contexto de requisição"""
    print("🧪 Testando template com contexto de requisição...")
    
    try:
        from app import create_app
        app = create_app()
        
        # Configurar SERVER_NAME para url_for funcionar
        app.config['SERVER_NAME'] = 'localhost:5000'
        
        with app.app_context():
            with app.test_request_context():
                from flask import render_template
                html = render_template('convite_recepcao.html')
                print(f"✅ Template renderizado com sucesso! ({len(html)} caracteres)")
                
                # Verificar se contém elementos importantes
                checks = [
                    ("título", "recepção" in html.lower()),
                    ("nomes", "iara" in html.lower() and "samuel" in html.lower()),
                    ("links", "href=" in html),
                    ("styles", "style=" in html)
                ]
                
                for nome, resultado in checks:
                    status = "✅" if resultado else "❌"
                    print(f"{status} {nome}: {'presente' if resultado else 'ausente'}")
                
                return True
                
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def teste_rota_completa():
    """Testa a rota completa incluindo o contexto"""
    print("\n🌐 Testando rota completa...")
    
    try:
        from app import create_app
        app = create_app()
        
        with app.test_client() as client:
            response = client.get('/convite-recepcao')
            print(f"📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                html = response.data.decode('utf-8')
                print(f"✅ Resposta completa ({len(html)} caracteres)")
                
                # Verificar elementos específicos
                if "url_for" in html:
                    print("⚠️ Template ainda contém url_for não processado")
                else:
                    print("✅ Todos os url_for foram processados")
                
                if "href=" in html:
                    print("✅ Links presentes no HTML")
                else:
                    print("❌ Links não encontrados")
                    
                return True
            else:
                print(f"❌ Erro HTTP: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Erro na rota: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Diagnóstico específico do url_for\n")
    
    teste1 = teste_template_com_contexto()
    teste2 = teste_rota_completa()
    
    print("\n" + "="*40)
    print("📋 RESUMO:")
    print(f"Template com contexto: {'✅' if teste1 else '❌'}")
    print(f"Rota completa: {'✅' if teste2 else '❌'}")
    
    if teste1 and teste2:
        print("\n🎉 O template está funcionando corretamente!")
        print("💡 O problema pode ser apenas quando testado fora do contexto.")
    else:
        print("\n⚠️ Há problemas que precisam ser corrigidos.")
