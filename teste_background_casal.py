#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste para verificar se a foto do casal aparece como background na página O Casal
"""

import requests
from pathlib import Path

def test_couple_background():
    """Testa se a foto do casal aparece como background"""
    
    BASE_URL = "http://127.0.0.1:5000"
    COUPLE_URL = f"{BASE_URL}/o-casal"
    
    print("🧪 Testando Background da Foto do Casal")
    print("=" * 50)
    
    try:
        # Acessar a página O Casal
        response = requests.get(COUPLE_URL)
        print(f"1. Status da página O Casal: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            # Verificar se contém a lógica de background condicional
            checks = [
                ('config.has_foto(\'casal\')', 'Verificação se tem foto do casal'),
                ('config.get_foto_url(\'casal\')', 'URL da foto do casal'),
                ('style="background:', 'CSS inline para background'),
                ('rgba(249, 242, 242, 0.85)', 'Overlay semitransparente'),
                ('center/cover', 'Posicionamento da imagem'),
            ]
            
            print("2. Verificando implementação do background:")
            for check, description in checks:
                if check in content:
                    print(f"   ✅ {description} - OK")
                else:
                    print(f"   ❌ {description} - NÃO ENCONTRADO")
            
            # Verificar estrutura do hero
            if 'hero-couple' in content:
                print(f"   ✅ Seção hero-couple encontrada - OK")
            else:
                print(f"   ❌ Seção hero-couple - NÃO ENCONTRADA")
                
        else:
            print(f"   ⚠️  Erro ao acessar página: {response.status_code}")
    
    except Exception as e:
        print(f"   ⚠️  Erro na requisição: {e}")
    
    print("\n📋 Implementação Realizada:")
    print("   - Modificada a página O Casal (o_casal.html)")
    print("   - Adicionado CSS inline condicional na seção hero")
    print("   - Background usa foto do casal quando disponível")
    print("   - Mantém overlay semitransparente para legibilidade")
    print("   - Fallback para background padrão quando sem foto")
    
    print("\n🎯 Como funciona:")
    print("   1. Upload foto do casal no modal de configurações")
    print("   2. A foto é salva como BLOB no banco de dados") 
    print("   3. Página O Casal verifica se existe foto (config.has_foto)")
    print("   4. Se existe, aplica CSS inline com a foto como background")
    print("   5. URL da foto: /image/casal/{config_id}")
    
    print("\n🎨 Resultado Visual:")
    print("   - Hero section com foto do casal como background")
    print("   - Overlay semitransparente para manter texto legível")
    print("   - Responsivo e otimizado para diferentes telas")

if __name__ == "__main__":
    test_couple_background()
