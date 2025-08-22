"""
Teste em tempo real - monitora o servidor para verificar se as requisições chegam
"""

import requests
import time

def teste_tempo_real():
    """Teste que você pode executar enquanto testa manualmente"""
    
    print("🕐 TESTE EM TEMPO REAL")
    print("=" * 50)
    print("📝 INSTRUÇÕES:")
    print("1. Execute este script")
    print("2. Em outra aba do navegador, acesse: http://localhost:5000/admin/login")
    print("3. Faça login com: master / master123")
    print("4. Vá para: http://localhost:5000/admin/presentes")
    print("5. Clique em um botão 'Remover'")
    print("6. Observe as mensagens abaixo...")
    print()
    
    session = requests.Session()
    
    # Fazer login primeiro
    print("🔐 Fazendo login automaticamente...")
    login_data = {'username': 'master', 'password': 'master123'}
    login_response = session.post("http://localhost:5000/admin/login", data=login_data)
    
    if "dashboard" in login_response.url:
        print("✅ Sistema pronto para teste!")
        print()
        
        # Listar presentes disponíveis
        presentes_response = session.get("http://localhost:5000/admin/presentes")
        
        import re
        ids = re.findall(r"onclick=\"confirmarRemocao\('(\d+)'", presentes_response.text)
        nomes = re.findall(r"<h3 class=\"presente-title\">([^<]+)</h3>", presentes_response.text)
        
        print("📦 PRESENTES DISPONÍVEIS PARA TESTE:")
        for i, (id_presente, nome) in enumerate(zip(ids[:5], nomes[:5])):
            print(f"   {i+1}. ID: {id_presente} - {nome}")
        print()
        
        print("🎯 AGUARDANDO VOCÊ CLICAR EM 'REMOVER'...")
        print("   (Verifique o terminal do servidor para logs)")
        print()
        
        # Loop para monitorar mudanças
        count_inicial = len(ids)
        
        for i in range(60):  # Monitor por 60 segundos
            time.sleep(1)
            
            try:
                # Verificar se houve mudança no número de presentes
                response = session.get("http://localhost:5000/admin/presentes")
                novos_ids = re.findall(r"onclick=\"confirmarRemocao\('(\d+)'", response.text)
                
                if len(novos_ids) != count_inicial:
                    print(f"🎉 MUDANÇA DETECTADA! Presentes: {count_inicial} → {len(novos_ids)}")
                    print("✅ O botão de exclusão FUNCIONOU!")
                    return
                    
                if i % 10 == 0:
                    print(f"⏱️  Aguardando... ({60-i}s restantes)")
                    
            except Exception as e:
                print(f"❌ Erro ao verificar: {e}")
        
        print("⏰ Tempo esgotado. Nenhuma mudança detectada.")
        print("🔍 Possíveis problemas:")
        print("   - JavaScript não está executando")
        print("   - Erro no navegador (verifique Console F12)")
        print("   - Sessão expirou")
        
    else:
        print("❌ Falha no login automático")

def teste_direto_api():
    """Teste direto da API para confirmar que funciona"""
    
    print("\n🔌 TESTE DIRETO DA API")
    print("-" * 30)
    
    session = requests.Session()
    
    # Login
    login_data = {'username': 'master', 'password': 'master123'}
    login_response = session.post("http://localhost:5000/admin/login", data=login_data)
    
    if "dashboard" in login_response.url:
        print("✅ Login OK")
        
        # Pegar lista de presentes
        presentes_response = session.get("http://localhost:5000/admin/presentes")
        
        import re
        ids = re.findall(r"onclick=\"confirmarRemocao\('(\d+)'", presentes_response.text)
        
        if ids:
            primeiro_id = ids[0]
            print(f"🎯 Testando remoção do presente ID: {primeiro_id}")
            
            # Tentar remover
            remove_response = session.post(f"http://localhost:5000/admin/presentes/{primeiro_id}/remover")
            
            print(f"📊 Status da resposta: {remove_response.status_code}")
            print(f"🔄 URL final: {remove_response.url}")
            
            if remove_response.status_code == 200 and "presentes" in remove_response.url:
                print("✅ API de remoção está funcionando perfeitamente!")
                
                # Verificar se realmente removeu
                nova_response = session.get("http://localhost:5000/admin/presentes")
                novos_ids = re.findall(r"onclick=\"confirmarRemocao\('(\d+)'", nova_response.text)
                
                if len(novos_ids) < len(ids):
                    print("🎉 Presente foi removido com sucesso!")
                    print("🔍 O problema deve estar no JavaScript do navegador")
                else:
                    print("⚠️  Presente não foi removido (pode ter restrições)")
            else:
                print("❌ Problema na API de remoção")
        else:
            print("❌ Nenhum presente encontrado")
    else:
        print("❌ Falha no login")

def main():
    print("🔬 DIAGNÓSTICO AVANÇADO DO BOTÃO DE EXCLUSÃO")
    print("=" * 60)
    
    # Aguardar servidor estabilizar
    time.sleep(2)
    
    # Primeiro teste direto da API
    teste_direto_api()
    
    # Depois teste em tempo real
    print("\n" + "=" * 60)
    teste_tempo_real()

if __name__ == "__main__":
    main()
