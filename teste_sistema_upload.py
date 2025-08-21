#!/usr/bin/env python3
"""
Script de teste para verificar o sistema completo de upload de imagens
"""

import requests
import json
from io import BytesIO
from PIL import Image

def criar_imagem_teste(cor, tamanho=(400, 300)):
    """Cria uma imagem de teste"""
    image = Image.new('RGB', tamanho, color=cor)
    buffer = BytesIO()
    image.save(buffer, format='JPEG')
    buffer.seek(0)
    return buffer

def testar_sistema_upload():
    """Testa o sistema completo de upload"""
    base_url = "http://127.0.0.1:5000"
    
    print("🧪 TESTE DO SISTEMA DE UPLOAD DE IMAGENS")
    print("=" * 50)
    
    # 1. Testar página inicial
    print("\n1. Testando página inicial...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Página inicial carregada com sucesso")
        else:
            print(f"❌ Erro na página inicial: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao acessar página inicial: {e}")
    
    # 2. Testar página de teste de imagens
    print("\n2. Testando página de teste de imagens...")
    try:
        response = requests.get(f"{base_url}/teste-imagens")
        if response.status_code == 200:
            print("✅ Página de teste carregada com sucesso")
            # Verificar se não há imagens configuradas inicialmente
            if "Placeholder" in response.text:
                print("✅ Placeholders funcionando corretamente")
        else:
            print(f"❌ Erro na página de teste: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao acessar página de teste: {e}")
    
    # 3. Testar página do casal
    print("\n3. Testando página do casal...")
    try:
        response = requests.get(f"{base_url}/o-casal")
        if response.status_code == 200:
            print("✅ Página do casal carregada com sucesso")
        else:
            print(f"❌ Erro na página do casal: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao acessar página do casal: {e}")
    
    # 4. Testar rota de servir imagens (sem imagem ainda)
    print("\n4. Testando rota de servir imagens...")
    try:
        response = requests.get(f"{base_url}/image/casal/1")
        if response.status_code == 404:
            print("✅ Rota responde corretamente quando não há imagem")
        else:
            print(f"⚠️ Resposta inesperada: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao testar rota de imagem: {e}")
    
    # 5. Verificar estrutura do banco
    print("\n5. Verificando estrutura do banco...")
    try:
        from app import create_app
        from app.models import ConfiguracaoSite, db
        
        app = create_app()
        with app.app_context():
            config = ConfiguracaoSite.query.first()
            if config:
                print("✅ ConfiguracaoSite encontrada no banco")
                
                # Verificar novos campos
                campos_blob = ['foto_casal_blob', 'foto_noiva_blob', 'foto_noivo_blob']
                campos_filename = ['foto_casal_filename', 'foto_noiva_filename', 'foto_noivo_filename']
                campos_mimetype = ['foto_casal_mimetype', 'foto_noiva_mimetype', 'foto_noivo_mimetype']
                
                todos_campos = campos_blob + campos_filename + campos_mimetype
                
                for campo in todos_campos:
                    if hasattr(config, campo):
                        print(f"✅ Campo {campo} existe")
                    else:
                        print(f"❌ Campo {campo} não encontrado")
                
                # Testar métodos
                try:
                    result = config.has_foto('casal')
                    print(f"✅ Método has_foto() funciona: {result}")
                except Exception as e:
                    print(f"❌ Erro no método has_foto(): {e}")
                
                try:
                    result = config.get_foto_url('casal')
                    print(f"✅ Método get_foto_url() funciona: {result}")
                except Exception as e:
                    print(f"❌ Erro no método get_foto_url(): {e}")
            else:
                print("⚠️ Nenhuma configuração encontrada no banco")
                
    except Exception as e:
        print(f"❌ Erro ao verificar banco: {e}")
    
    print("\n" + "=" * 50)
    print("✅ TESTE CONCLUÍDO")
    print("\n🔧 PRÓXIMOS PASSOS:")
    print("1. Acesse http://127.0.0.1:5000/admin para fazer login")
    print("2. Vá em Configurações para testar o upload")
    print("3. Verifique http://127.0.0.1:5000/teste-imagens para diagnosticar")
    print("4. Teste http://127.0.0.1:5000/o-casal para ver as fotos")

if __name__ == "__main__":
    testar_sistema_upload()
