"""
Teste específico para verificar a funcionalidade de exclusão de presentes
na página de lista de presentes (admin/presentes)
"""

import requests
import time

def teste_exclusao_presentes():
    """Testa a exclusão de presentes da página de lista"""
    
    print("🧪 TESTE: Exclusão de Presentes da Lista")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # 1. Verificar se a página de presentes carrega
    print("\n1. 📄 Verificando página de presentes...")
    try:
        response = requests.get(f"{base_url}/admin/presentes")
        print(f"   Status: {response.status_code}")
        
        if "confirmarRemocao" in response.text:
            print("   ✅ Função JavaScript encontrada")
        else:
            print("   ❌ Função JavaScript NÃO encontrada")
            
        if "btn-danger" in response.text:
            print("   ✅ Botões de remoção encontrados")
        else:
            print("   ❌ Botões de remoção NÃO encontrados")
            
    except Exception as e:
        print(f"   ❌ Erro ao acessar página: {e}")
    
    # 2. Verificar se existem presentes para testar
    print("\n2. 📦 Verificando presentes disponíveis...")
    try:
        # Tentar acessar a rota de presentes e procurar por IDs
        if "presente-card" in response.text:
            print("   ✅ Presentes encontrados na página")
            
            # Extrair IDs dos presentes do HTML
            import re
            ids = re.findall(r"onclick=\"confirmarRemocao\('(\d+)'", response.text)
            print(f"   📋 IDs encontrados: {ids}")
            
            if ids:
                print(f"   ✅ {len(ids)} presente(s) disponível(is) para teste")
                return ids[0]  # Retorna o primeiro ID para teste
            else:
                print("   ⚠️  Nenhum ID de presente encontrado no JavaScript")
        else:
            print("   ⚠️  Nenhum presente encontrado na página")
            
    except Exception as e:
        print(f"   ❌ Erro ao verificar presentes: {e}")
    
    return None

def verificar_javascript_estrutura():
    """Verifica se a estrutura do JavaScript está correta"""
    
    print("\n3. 🔧 Verificando estrutura do JavaScript...")
    
    # Ler o arquivo de template
    try:
        with open("app/templates/admin/presentes.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Verificar elementos essenciais
        checks = [
            ("function confirmarRemocao", "Função confirmarRemocao definida"),
            ("form.method = 'POST'", "Método POST configurado"),
            ("form.action = ", "Action do formulário configurado"),
            ("/remover", "Rota de remoção presente"),
            ("form.submit()", "Submit do formulário"),
            ("confirm(", "Confirmação do usuário")
        ]
        
        for check, desc in checks:
            if check in content:
                print(f"   ✅ {desc}")
            else:
                print(f"   ❌ {desc} - FALTANDO")
                
        # Verificar se a rota está correta
        if "/admin/presentes/${presenteId}/remover" in content:
            print("   ✅ Rota correta configurada")
        else:
            print("   ❌ Rota incorreta ou não encontrada")
            
    except Exception as e:
        print(f"   ❌ Erro ao verificar template: {e}")

def main():
    print("🚀 INICIANDO DIAGNÓSTICO DE EXCLUSÃO DE PRESENTES")
    print("=" * 60)
    
    # Aguardar o servidor inicializar
    print("⏳ Aguardando servidor...")
    time.sleep(2)
    
    # Executar testes
    verificar_javascript_estrutura()
    primeiro_id = teste_exclusao_presentes()
    
    print("\n" + "=" * 60)
    print("📋 RESUMO DO DIAGNÓSTICO:")
    
    if primeiro_id:
        print(f"✅ Sistema aparenta estar configurado corretamente")
        print(f"📝 ID de teste disponível: {primeiro_id}")
        print(f"🖱️  Para testar manualmente:")
        print(f"   1. Acesse: http://localhost:5000/admin/presentes")
        print(f"   2. Clique no botão 'Remover' de qualquer presente")
        print(f"   3. Confirme a exclusão no popup")
        print(f"   4. Verifique se o presente foi removido")
    else:
        print("⚠️  Possíveis problemas encontrados")
        print("🔧 Verificar se há presentes cadastrados")
        print("🔧 Verificar se o JavaScript está carregando corretamente")
    
    print("\n🏁 Diagnóstico concluído!")

if __name__ == "__main__":
    main()
