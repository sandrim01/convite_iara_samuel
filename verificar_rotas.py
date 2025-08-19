#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificar rotas registradas no Flask
"""
from app import create_app

app = create_app()

with app.app_context():
    print("🔍 Rotas registradas no Flask:")
    print("="*50)
    
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods - {'HEAD', 'OPTIONS'})
        print(f"{rule.endpoint:30} {methods:10} {rule.rule}")
    
    print("="*50)
    print(f"Total de rotas: {len(list(app.url_map.iter_rules()))}")
    
    # Verificar especificamente as rotas de presentes
    print("\n🎁 Rotas de presentes:")
    for rule in app.url_map.iter_rules():
        if 'presente' in rule.rule.lower():
            methods = ','.join(rule.methods - {'HEAD', 'OPTIONS'})
            print(f"  {rule.endpoint:30} {methods:10} {rule.rule}")
