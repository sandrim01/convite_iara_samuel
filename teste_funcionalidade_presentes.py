#!/usr/bin/env python3

"""
Teste específico da funcionalidade de adicionar presente por link
"""

import requests
import sys
import json

def testar_adicionar_presente_por_link():
    """Testa especificamente a funcionalidade de adicionar presente por link"""
    base_url = "http://127.0.0.1:5000"
    
    print("🔍 TESTE ESPECÍFICO: ADICIONAR PRESENTE POR LINK\n")
    
    # Criar sessão
    session = requests.Session()
    
    try:
        # 1. Fazer login
        print("1️⃣ Fazendo login no admin...")
        login_url = f"{base_url}/admin/login"
        login_data = {
            'username': 'admin',
            'password': 'Casamento2025*#'
        }
        
        response = session.post(login_url, data=login_data, timeout=5)
        if response.status_code not in [200, 302]:
            print(f"❌ Erro no login: {response.status_code}")
            return False
        print("✅ Login realizado com sucesso")
        
        # 2. Acessar página de presentes
        print("\n2️⃣ Acessando página de presentes...")
        presentes_url = f"{base_url}/admin/presentes"
        response = session.get(presentes_url, timeout=5)
        if response.status_code != 200:
            print(f"❌ Erro ao acessar presentes: {response.status_code}")
            return False
        print("✅ Página de presentes carregada")
        
        # Verificar se tem o campo de link
        content = response.text
        if "Link do Produto" in content or "link" in content.lower():
            print("✅ Campo de adicionar por link encontrado na página")
        else:
            print("⚠️ Campo de link pode não estar presente")
            print("🔍 Buscando por 'adicionarPresentePorLink' no código...")
            if "adicionarPresentePorLink" in content:
                print("✅ Função JavaScript encontrada")
            else:
                print("❌ Função JavaScript não encontrada")
        
        # 3. Testar a rota de adicionar por link
        print("\n3️⃣ Testando rota de adicionar presente por link...")
        link_url = f"{base_url}/admin/adicionar-presente-por-link"
        test_data = {
            'link': 'https://exemplo.com/produto-teste'
        }
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        response = session.post(link_url, json=test_data, headers=headers, timeout=10)
        print(f"Status da requisição: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"Resposta JSON: {result}")
                
                if result.get('success'):
                    print("✅ Funcionalidade de adicionar por link funcionando!")
                    return True
                else:
                    print(f"⚠️ Resposta indica erro: {result.get('error', 'Erro desconhecido')}")
            except json.JSONDecodeError:
                print("❌ Resposta não é JSON válido")
                print(f"Resposta: {response.text[:200]}")
        else:
            print(f"❌ Erro na requisição: {response.status_code}")
            print(f"Resposta: {response.text[:200]}")
        
        # 4. Verificar se a rota existe
        print("\n4️⃣ Verificando rotas disponíveis...")
        try:
            # Tentar diferentes variações da URL
            variations = [
                f"{base_url}/admin/adicionar-presente-por-link",
                f"{base_url}/admin/adicionar_presente_por_link",
                f"{base_url}/admin/presentes/adicionar-por-link"
            ]
            
            for var_url in variations:
                resp = session.post(var_url, json=test_data, headers=headers, timeout=5)
                print(f"   {var_url}: {resp.status_code}")
                if resp.status_code == 200:
                    print(f"   ✅ Rota funcionando: {var_url}")
                    break
        except Exception as e:
            print(f"   Erro testando variações: {e}")
        
        return False
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        return False

def verificar_template_presentes():
    """Verifica o conteúdo do template de presentes"""
    print("\n🔍 VERIFICANDO TEMPLATE DE PRESENTES")
    
    try:
        with open("app/templates/admin/presentes.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Verificar elementos essenciais
        checks = [
            ("Campo de link", "Link do Produto" in content or 'id="linkProduto"' in content),
            ("Função JavaScript", "adicionarPresentePorLink" in content),
            ("Botão de enviar", 'type="submit"' in content or "onclick" in content),
            ("URL da API", "/admin/adicionar-presente-por-link" in content or "/admin/adicionar_presente_por_link" in content)
        ]
        
        for name, check in checks:
            status = "✅" if check else "❌"
            print(f"   {status} {name}")
            
        return all(check for _, check in checks)
        
    except FileNotFoundError:
        print("❌ Template presentes.html não encontrado")
        return False
    except Exception as e:
        print(f"❌ Erro ao verificar template: {e}")
        return False

if __name__ == "__main__":
    print("🧪 TESTE COMPLETO DE FUNCIONALIDADE\n")
    
    # Verificar template
    template_ok = verificar_template_presentes()
    
    # Testar funcionalidade
    funcionalidade_ok = testar_adicionar_presente_por_link()
    
    print(f"\n📋 RESULTADOS:")
    print(f"   Template: {'✅ OK' if template_ok else '❌ Problema'}")
    print(f"   Funcionalidade: {'✅ OK' if funcionalidade_ok else '❌ Problema'}")
    
    if template_ok and funcionalidade_ok:
        print(f"\n🎉 TUDO FUNCIONANDO PERFEITAMENTE!")
        print(f"   Acesse: http://127.0.0.1:5000/admin/presentes")
        print(f"   Cole um link de produto no campo e teste!")
    else:
        print(f"\n💥 PROBLEMA IDENTIFICADO!")
        print(f"   O template ou a funcionalidade precisa ser corrigida.")
        sys.exit(1)
