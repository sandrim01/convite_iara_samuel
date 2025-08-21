#!/usr/bin/env python3
"""
Teste final do upload de imagens
"""

import requests
import time
from PIL import Image
from io import BytesIO
import json

def teste_upload_final():
    print("🧪 TESTE FINAL DO UPLOAD DE IMAGENS")
    print("=" * 50)
    
    # Aguardar servidor
    print("1. Aguardando servidor inicializar...")
    time.sleep(2)
    
    # Criar imagem de teste
    print("2. Criando imagem de teste...")
    try:
        img = Image.new('RGB', (300, 300), color='#B91C1C')  # Cor do tema
        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=90)
        buffer.seek(0)
        print("✅ Imagem criada com sucesso")
    except Exception as e:
        print(f"❌ Erro ao criar imagem: {e}")
        return
    
    # Fazer upload
    print("3. Fazendo upload...")
    try:
        files = {'foto': ('teste_casal.jpg', buffer, 'image/jpeg')}
        data = {'tipo': 'casal'}
        
        response = requests.post('http://127.0.0.1:5000/admin/teste-upload-foto', 
                               files=files, data=data, timeout=10)
        
        print(f"Status HTTP: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                if result.get('success'):
                    print("✅ UPLOAD REALIZADO COM SUCESSO!")
                    print(f"URL da imagem: {result.get('url')}")
                    print(f"Mensagem: {result.get('message')}")
                    
                    # Testar se a imagem pode ser acessada
                    print("4. Testando acesso à imagem...")
                    image_url = result.get('url')
                    if image_url:
                        full_url = f"http://127.0.0.1:5000{image_url}"
                        img_response = requests.get(full_url, timeout=5)
                        if img_response.status_code == 200:
                            print("✅ Imagem acessível com sucesso!")
                        else:
                            print(f"⚠️ Imagem não acessível: {img_response.status_code}")
                else:
                    print(f"❌ Erro no upload: {result.get('error')}")
            except json.JSONDecodeError:
                print("❌ Resposta não é JSON válido")
                print(f"Conteúdo: {response.text[:200]}...")
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            print(f"Resposta: {response.text[:200]}...")
            
    except requests.ConnectionError:
        print("❌ Erro de conexão - servidor não está rodando")
    except requests.Timeout:
        print("❌ Timeout - servidor demorou para responder")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 PRÓXIMOS PASSOS:")
    print("1. Se o upload funcionou, acesse: http://127.0.0.1:5000/teste-imagens")
    print("2. Vá para: http://127.0.0.1:5000/o-casal")
    print("3. Login admin: http://127.0.0.1:5000/admin")
    print("4. Teste interface completa em: Configurações > Fotos dos Noivos")

if __name__ == "__main__":
    teste_upload_final()
