from app import create_app
from flask import render_template

app = create_app()

with app.app_context():
    print("🔍 Testando template local.html...")
    
    try:
        # Testar se conseguimos renderizar o template
        from app.models import ConfiguracaoSite
        from datetime import datetime
        
        config = ConfiguracaoSite.query.first()
        if not config:
            config = ConfiguracaoSite(
                nome_noiva='Iara',
                nome_noivo='Samuel',
                data_casamento=datetime(2025, 11, 8).date(),
                local_cerimonia='Igreja Nossa Senhora das Graças'
            )
        
        # Calcular dias restantes
        if config.data_casamento:
            hoje = datetime.now().date()
            dias_restantes = (config.data_casamento - hoje).days
            data_limite = config.data_casamento
        else:
            dias_restantes = 0
            data_limite = None
        
        html = render_template('local.html', config=config, dias_restantes=dias_restantes, data_limite=data_limite)
        print(f"✅ Template renderizado com sucesso! ({len(html)} caracteres)")
        
    except Exception as e:
        print(f"❌ Erro ao renderizar template: {e}")
        import traceback
        traceback.print_exc()
