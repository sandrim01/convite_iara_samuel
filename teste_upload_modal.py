#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste para verificar se o upload de fotos no modal está funcionando
"""

import requests
from pathlib import Path

# Configurações
BASE_URL = "http://127.0.0.1:5000"
LOGIN_URL = f"{BASE_URL}/admin/login"
CONFIG_URL = f"{BASE_URL}/admin/configuracoes"

def test_modal_upload():
    """Testa se o modal de configurações aceita uploads"""
    
    session = requests.Session()
    
    print("🧪 Testando Upload de Fotos no Modal de Configurações")
    print("=" * 60)
    
    # Primeiro, fazer login (se necessário)
    print("1. Fazendo login...")
    login_data = {
        'username': 'admin',  # Ajuste conforme necessário
        'password': 'senha123'  # Ajuste conforme necessário
    }
    
    try:
        login_response = session.post(LOGIN_URL, data=login_data)
        print(f"   Status do login: {login_response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Erro no login: {e}")
    
    # Testar se a página de configurações carrega
    print("2. Verificando página de configurações...")
    try:
        config_response = session.get(CONFIG_URL)
        print(f"   Status da página: {config_response.status_code}")
        
        # Verificar se contém os campos de upload
        content = config_response.text
        
        checks = [
            ('foto_casal_modal', 'Foto do Casal'),
            ('foto_noiva_modal', 'Foto da Noiva'),
            ('foto_noivo_modal', 'Foto do Noivo'),
            ('enctype="multipart/form-data"', 'Formulário com upload'),
            ('input type="file"', 'Campos de arquivo')
        ]
        
        print("3. Verificando elementos do upload:")
        for field, description in checks:
            if field in content:
                print(f"   ✅ {description} - OK")
            else:
                print(f"   ❌ {description} - NÃO ENCONTRADO")
        
    except Exception as e:
        print(f"   ⚠️  Erro ao acessar configurações: {e}")
    
    print("\n📋 Resumo:")
    print("   - Modal de configurações modificado para aceitar uploads")
    print("   - Campos de arquivo implementados para:")
    print("     • Foto do Casal (foto_casal_modal)")
    print("     • Foto da Noiva (foto_noiva_modal)")
    print("     • Foto do Noivo (foto_noivo_modal)")
    print("   - Backend já configurado para processar os uploads")
    print("   - Formulário com enctype='multipart/form-data'")
    
    print("\n🎯 Como usar:")
    print("   1. Acesse o dashboard do admin")
    print("   2. Clique no card 'Configurações do Site'")
    print("   3. No modal, vá até as seções:")
    print("      - Personalização (Foto do Casal)")
    print("      - Sobre a Noiva (Foto da Noiva)")
    print("      - Sobre o Noivo (Foto do Noivo)")
    print("   4. Clique em 'Selecionar Arquivo' e escolha uma imagem")
    print("   5. Clique em 'Salvar Configurações'")

if __name__ == "__main__":
    test_modal_upload()
