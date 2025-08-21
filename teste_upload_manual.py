#!/usr/bin/env python3
"""
Script para testar o upload de imagens
"""

import requests
from io import BytesIO
from PIL import Image
import json

def criar_imagem_teste(cor='#FF0000', tamanho=(300, 300)):
    """Cria uma imagem de teste simples"""
    # Criar uma imagem colorida
    image = Image.new('RGB', tamanho, color=cor)
    
    # Adicionar um texto simples
    from PIL import ImageDraw
    draw = ImageDraw.Draw(image)
    draw.rectangle([(50, 50), (250, 250)], fill='white', outline='black', width=3)
    
    # Salvar em buffer
    buffer = BytesIO()
    image.save(buffer, format='JPEG', quality=90)
    buffer.seek(0)
    
    return buffer

def testar_upload():
    """Testa o upload de uma imagem"""
    print("🧪 TESTE DE UPLOAD DE IMAGEM")
    print("=" * 40)
    
    # Criar uma sessão para manter cookies
    session = requests.Session()
    
    print("1. Testando se a rota existe...")
    try:
        # Primeiro, testar se a rota responde (mesmo que com erro de autenticação)
        response = session.get("http://127.0.0.1:5000/admin/upload-foto")
        print(f"Status da rota: {response.status_code}")
        
        if response.status_code == 405:
            print("✅ Rota existe (erro 405 = método não permitido, esperado)")
        elif response.status_code == 302:
            print("✅ Rota existe (302 = redirecionamento para login, esperado)")
        else:
            print(f"⚠️ Status inesperado: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro ao acessar rota: {e}")
        return
    
    # Criar imagem de teste
    print("2. Criando imagem de teste...")
    try:
        image_buffer = criar_imagem_teste('#B91C1C')  # Cor do tema
        print("✅ Imagem criada com sucesso")
    except Exception as e:
        print(f"❌ Erro ao criar imagem: {e}")
        return
    
    # Testar upload (sem autenticação primeiro)
    print("3. Testando upload (sem autenticação)...")
    try:
        url = "http://127.0.0.1:5000/admin/upload-foto"
        
        files = {
            'foto': ('teste.jpg', image_buffer, 'image/jpeg')
        }
        
        data = {
            'tipo': 'casal'
        }
        
        response = session.post(url, files=files, data=data)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 302:
            print("✅ Redirecionamento esperado (precisa de autenticação)")
        elif response.status_code == 401:
            print("✅ Não autorizado (precisa de autenticação)")
        elif response.status_code == 200:
            print("✅ Upload funcionou!")
            try:
                json_response = response.json()
                print(f"Resposta: {json_response}")
            except:
                print(f"Resposta HTML: {response.text[:200]}...")
        else:
            print(f"⚠️ Status inesperado: {response.status_code}")
            print(f"Resposta: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
    
    print("\n4. Testando página de administração...")
    try:
        admin_response = session.get("http://127.0.0.1:5000/admin")
        print(f"Admin status: {admin_response.status_code}")
        
        if admin_response.status_code == 200:
            print("✅ Página admin acessível")
        else:
            print(f"⚠️ Página admin com status: {admin_response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro ao acessar admin: {e}")
        
    print("\n🔧 Para testar o upload completo:")
    print("1. Acesse http://127.0.0.1:5000/admin")
    print("2. Faça login como administrador")
    print("3. Vá em 'Configurações'")
    print("4. Teste o upload na seção 'Fotos dos Noivos'")

if __name__ == "__main__":
    testar_upload()
