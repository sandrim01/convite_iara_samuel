#!/usr/bin/env python3
"""
Teste do template convite_recepcao.html
"""

from jinja2 import Environment, FileSystemLoader
import os
from datetime import datetime, date, time

def teste_template():
    try:
        # Verificar se o template é válido
        env = Environment(loader=FileSystemLoader('app/templates'))
        template = env.get_template('convite_recepcao.html')
        print('✅ Template carregado com sucesso!')
        
        # Testar renderização básica
        context = {
            'config': {
                'nome_noiva': 'Iara',
                'nome_noivo': 'Samuel',
                'data_casamento': date(2025, 12, 15),
                'horario_festa': time(18, 0),
                'local_festa': 'Salão de Festas Elegance',
                'endereco_festa': 'Av. Principal, 456 - Jardim das Rosas',
                'telefone_contato': '(11) 99999-9999',
                'whatsapp': '5511999999999'
            }
        }
        
        rendered = template.render(context)
        print('✅ Template renderizado com sucesso!')
        print(f'Tamanho do HTML: {len(rendered)} caracteres')
        
        # Verificar se há problemas específicos no HTML
        if 'error' in rendered.lower():
            print('⚠️  Possível erro encontrado no HTML renderizado')
        
        # Verificar estruturas básicas
        if '<html>' in rendered or '{% extends' in rendered:
            print('✅ Estrutura HTML básica presente')
        else:
            print('❌ Estrutura HTML pode estar incorreta')
            
        return True
        
    except Exception as e:
        print(f'❌ Erro no template: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    teste_template()
