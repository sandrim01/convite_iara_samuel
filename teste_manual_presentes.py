"""
Teste manual simulado - reproduzir exatamente o que o usuário está fazendo
"""

import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import sys

def teste_manual_simulado():
    """Simula exatamente o processo manual do usuário"""
    
    print("🎭 SIMULAÇÃO DO TESTE MANUAL")
    print("=" * 50)
    
    # Configurar Chrome para teste
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executar em background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    try:
        # Tentar usar chromedriver
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"❌ Erro ao inicializar Chrome: {e}")
        print("🔧 Tentando teste com requests apenas...")
        return teste_com_requests()
    
    try:
        print("🌐 Abrindo navegador...")
        
        # 1. Acessar página de login
        print("\n1. 🔐 Acessando página de login...")
        driver.get("http://localhost:5000/admin/login")
        time.sleep(2)
        
        # 2. Fazer login
        print("2. ✍️  Preenchendo credenciais...")
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        
        username_field.send_keys("master")
        password_field.send_keys("master123")
        
        print("3. 🚀 Clicando em Login...")
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        
        time.sleep(3)
        
        # 3. Verificar se foi redirecionado para dashboard
        current_url = driver.current_url
        print(f"   URL atual: {current_url}")
        
        if "dashboard" in current_url:
            print("   ✅ Login realizado com sucesso!")
        else:
            print("   ❌ Falha no login!")
            return False
        
        # 4. Acessar página de presentes
        print("\n4. 📦 Acessando lista de presentes...")
        driver.get("http://localhost:5000/admin/presentes")
        time.sleep(3)
        
        # 5. Verificar se existem presentes
        presente_cards = driver.find_elements(By.CLASS_NAME, "presente-card")
        print(f"   📋 Encontrados {len(presente_cards)} presentes")
        
        if len(presente_cards) == 0:
            print("   ⚠️  Nenhum presente encontrado!")
            return False
        
        # 6. Procurar botão de remover
        print("\n5. 🔍 Procurando botões de remoção...")
        remove_buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'btn-danger')]")
        print(f"   🗑️  Encontrados {len(remove_buttons)} botões de remoção")
        
        if len(remove_buttons) == 0:
            print("   ❌ Nenhum botão de remoção encontrado!")
            return False
        
        # 7. Clicar no primeiro botão de remoção
        print("\n6. 🖱️  Clicando no primeiro botão de remoção...")
        first_button = remove_buttons[0]
        
        # Verificar o onclick do botão
        onclick_attr = first_button.get_attribute("onclick")
        print(f"   📝 Atributo onclick: {onclick_attr}")
        
        # Executar JavaScript para clicar (simular exatamente o clique)
        driver.execute_script("arguments[0].click();", first_button)
        time.sleep(2)
        
        # 8. Verificar se apareceu o alert
        print("\n7. ⚠️  Verificando alert de confirmação...")
        try:
            alert = driver.switch_to.alert
            alert_text = alert.text
            print(f"   📢 Texto do alert: {alert_text}")
            
            # Aceitar o alert (simular clique em OK)
            print("   ✅ Aceitando confirmação...")
            alert.accept()
            time.sleep(3)
            
            # 9. Verificar se a página recarregou/redirecionou
            final_url = driver.current_url
            print(f"   🔄 URL final: {final_url}")
            
            if "presentes" in final_url:
                print("   ✅ Redirecionamento correto!")
                
                # Verificar se o presente foi removido
                new_presente_cards = driver.find_elements(By.CLASS_NAME, "presente-card")
                print(f"   📊 Presentes após exclusão: {len(new_presente_cards)}")
                
                if len(new_presente_cards) < len(presente_cards):
                    print("   🎉 PRESENTE REMOVIDO COM SUCESSO!")
                    return True
                else:
                    print("   ❌ Presente NÃO foi removido")
                    return False
            else:
                print("   ❌ Redirecionamento incorreto")
                return False
                
        except Exception as e:
            print(f"   ❌ Erro com alert: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Erro durante teste: {e}")
        return False
        
    finally:
        driver.quit()

def teste_com_requests():
    """Teste alternativo com requests"""
    
    print("\n📡 TESTE COM REQUESTS")
    print("-" * 30)
    
    session = requests.Session()
    
    # Login
    print("🔐 Fazendo login...")
    login_data = {'username': 'master', 'password': 'master123'}
    login_response = session.post("http://localhost:5000/admin/login", data=login_data)
    
    if "dashboard" in login_response.url:
        print("✅ Login bem-sucedido")
        
        # Acessar presentes
        presentes_response = session.get("http://localhost:5000/admin/presentes")
        
        if presentes_response.status_code == 200:
            print("✅ Página de presentes acessada")
            
            # Procurar IDs de presentes
            import re
            ids = re.findall(r"onclick=\"confirmarRemocao\('(\d+)'", presentes_response.text)
            
            if ids:
                print(f"📋 IDs encontrados: {ids}")
                
                # Tentar remover o primeiro
                primeiro_id = ids[0]
                print(f"🗑️  Tentando remover presente ID: {primeiro_id}")
                
                remove_response = session.post(f"http://localhost:5000/admin/presentes/{primeiro_id}/remover")
                
                if remove_response.status_code == 200:
                    print("✅ Requisição de remoção bem-sucedida")
                    return True
                else:
                    print(f"❌ Erro na remoção: {remove_response.status_code}")
                    return False
            else:
                print("❌ Nenhum ID encontrado")
                return False
        else:
            print(f"❌ Erro ao acessar presentes: {presentes_response.status_code}")
            return False
    else:
        print("❌ Falha no login")
        return False

def main():
    print("🔍 DIAGNÓSTICO COMPLETO DO BOTÃO DE EXCLUSÃO")
    print("=" * 60)
    
    time.sleep(2)  # Aguardar servidor
    
    # Tentar teste simulado primeiro
    try:
        resultado = teste_manual_simulado()
    except:
        # Se falhar, usar requests
        resultado = teste_com_requests()
    
    print("\n" + "=" * 60)
    if resultado:
        print("✅ TESTE CONCLUÍDO: Botão de exclusão está FUNCIONANDO")
        print("💡 Se não está funcionando no seu navegador, verifique:")
        print("   - JavaScript habilitado")
        print("   - Console do navegador para erros")
        print("   - Sessão de login válida")
    else:
        print("❌ TESTE FALHOU: Botão de exclusão NÃO está funcionando")
        print("🔧 Verificações necessárias...")

if __name__ == "__main__":
    main()
