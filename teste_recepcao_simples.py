#!/usr/bin/env python3
"""
Teste simples para o convite de recepção
"""

import requests
import time

def teste_convite_recepcao():
    print("🧪 Testando convite de recepção...")
    
    try:
        url = "http://127.0.0.1:5000/convite-recepcao"
        print(f"📡 Fazendo requisição para: {url}")
        
        response = requests.get(url, timeout=10)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Sucesso! Convite de recepção está funcionando!")
            print(f"📄 Tamanho da resposta: {len(response.text)} caracteres")
            
            # Verificar conteúdo básico
            content = response.text.lower()
            checks = [
                ("recepção", "recepção" in content),
                ("casamento", "casamento" in content),
                ("iara", "iara" in content),
                ("samuel", "samuel" in content)
            ]
            
            for check_name, check_result in checks:
                status = "✅" if check_result else "❌"
                print(f"{status} {check_name}: {'presente' if check_result else 'ausente'}")
                
            return True
            
        elif response.status_code == 500:
            print("❌ Erro 500 - Erro interno do servidor")
            print("Detalhes do erro:")
            print(response.text[:1000])
            return False
            
        else:
            print(f"⚠️ Status code inesperado: {response.status_code}")
            print("Resposta:")
            print(response.text[:500])
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão - servidor não está rodando na porta 5000")
        return False
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {str(e)}")
        return False

if __name__ == "__main__":
    # Aguardar um pouco para o servidor estar pronto
    print("⏳ Aguardando servidor...")
    time.sleep(2)
    
    sucesso = teste_convite_recepcao()
    
    if sucesso:
        print("\n🎉 Teste concluído com sucesso!")
    else:
        print("\n⚠️ Teste falhou - verifique os detalhes acima.")
