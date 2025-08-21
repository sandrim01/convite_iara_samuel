from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file, abort
from app.models import db, ConfiguracaoSite, Convidado, Presente, EscolhaPresente
from datetime import datetime
from io import BytesIO
from PIL import Image
import os

main = Blueprint('main', __name__)

def process_image(file_data, max_size=(800, 800), quality=85):
    """Processa e redimensiona uma imagem"""
    try:
        # Abrir a imagem
        image = Image.open(BytesIO(file_data))
        
        # Converter para RGB se necessário (para JPEG)
        if image.mode in ('RGBA', 'LA', 'P'):
            image = image.convert('RGB')
        
        # Redimensionar mantendo proporção
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Salvar em bytes
        output = BytesIO()
        image.save(output, format='JPEG', quality=quality, optimize=True)
        output.seek(0)
        
        return output.getvalue()
    except Exception as e:
        print(f"Erro ao processar imagem: {e}")
        return None

def allowed_file(filename):
    """Verifica se o arquivo é uma imagem válida"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def index():
    """Página principal do convite"""
    config = ConfiguracaoSite.query.first()
    if not config:
        # Criar configuração padrão se não existir
        config = ConfiguracaoSite(
            nome_noiva='Iara',
            nome_noivo='Samuel',
            data_casamento=datetime(2025, 11, 8).date(),
            local_cerimonia='Igreja Nossa Senhora das Graças',
            endereco_cerimonia='Rua Domingos Alcíno Dadalto, 114, Jardim Itapemirim, Cachoeiro de Itapemirim - ES',
            horario_cerimonia=datetime.strptime('19:00', '%H:%M').time(),
            local_festa='Espaço Jardim Encantado',
            endereco_festa='Av. Paulista, 456 - Bela Vista, São Paulo - SP',
            horario_festa=datetime.strptime('20:00', '%H:%M').time(),
            mensagem_principal='Criamos esse site para compartilhar com vocês os detalhes da organização do nosso casamento. ♥'
        )
        db.session.add(config)
        db.session.commit()
    
    # Calcular dias restantes
    if config.data_casamento:
        hoje = datetime.now().date()
        dias_restantes = (config.data_casamento - hoje).days
    else:
        dias_restantes = 0
    
    return render_template('index.html', config=config, dias_restantes=dias_restantes)

@main.route('/o-casal')
def o_casal():
    """Página sobre o casal"""
    config = ConfiguracaoSite.query.first()
    if not config:
        config = ConfiguracaoSite(
            nome_noiva='Iara',
            nome_noivo='Samuel'
        )
    
    return render_template('o_casal.html', config=config)

@main.route('/teste-imagens')
def teste_imagens():
    """Página de teste para verificar se as imagens estão funcionando"""
    config = ConfiguracaoSite.query.first()
    if not config:
        config = ConfiguracaoSite(
            nome_noiva='Iara',
            nome_noivo='Samuel'
        )
    
    return render_template('teste_imagens.html', config=config)

@main.route('/image/<tipo>/<int:config_id>')
def serve_image(tipo, config_id):
    """Serve imagens armazenadas no banco de dados"""
    config = ConfiguracaoSite.query.get_or_404(config_id)
    
    if tipo == 'casal':
        image_data = config.foto_casal_blob
        mimetype = config.foto_casal_mimetype or 'image/jpeg'
        filename = config.foto_casal_filename or 'casal.jpg'
    elif tipo == 'noiva':
        image_data = config.foto_noiva_blob
        mimetype = config.foto_noiva_mimetype or 'image/jpeg'
        filename = config.foto_noiva_filename or 'noiva.jpg'
    elif tipo == 'noivo':
        image_data = config.foto_noivo_blob
        mimetype = config.foto_noivo_mimetype or 'image/jpeg'
        filename = config.foto_noivo_filename or 'noivo.jpg'
    else:
        abort(404)
    
    if not image_data:
        abort(404)
    
    return send_file(
        BytesIO(image_data),
        mimetype=mimetype,
        as_attachment=False,
        download_name=filename
    )

@main.route('/local')
@main.route('/local-teste')  # Rota adicional para teste
def local():
    """Página do local da cerimônia com confirmação de presença"""
    config = ConfiguracaoSite.query.first()
    if not config:
        config = ConfiguracaoSite(
            nome_noiva='Iara',
            nome_noivo='Samuel',
            data_casamento=datetime(2025, 11, 8).date(),
            local_cerimonia='Igreja Nossa Senhora das Graças',
            endereco_cerimonia='Rua Domingos Alcíno Dadalto, 114, Jardim Itapemirim, Cachoeiro de Itapemirim - ES',
            horario_cerimonia=datetime.strptime('19:00', '%H:%M').time()
        )
    
    # Calcular dias restantes
    if config.data_casamento:
        hoje = datetime.now().date()
        dias_restantes = (config.data_casamento - hoje).days
        data_limite = config.data_casamento
    else:
        dias_restantes = 0
        data_limite = None
    
    return render_template('local.html', config=config, dias_restantes=dias_restantes, data_limite=data_limite)

@main.route('/processar-confirmacao', methods=['POST'])
def processar_confirmacao():
    """Processar confirmação de presença"""
    nome = request.form.get('nome')
    telefone = request.form.get('telefone')
    email = request.form.get('email')
    acompanhantes = int(request.form.get('acompanhantes', 0))
    observacoes = request.form.get('observacoes')
    
    if not nome:
        flash('Nome é obrigatório', 'error')
        return redirect(url_for('main.local'))
    
    # Verificar se já existe um convidado com esse nome
    convidado_existente = Convidado.query.filter_by(nome=nome).first()
    
    if convidado_existente:
        flash('Já existe uma confirmação com esse nome. Entre em contato conosco se precisar fazer alterações.', 'warning')
        return redirect(url_for('main.local'))
    
    # Gerar token único para o convidado
    import uuid
    token = str(uuid.uuid4())
    
    # Criar novo convidado
    novo_convidado = Convidado(
        nome=nome,
        telefone=telefone,
        email=email,
        numero_acompanhantes=acompanhantes,
        mensagem=observacoes,
        token=token,
        confirmacao=True,
        data_confirmacao=datetime.utcnow(),
        liberado_recepcao=True  # Liberar automaticamente para recepção
    )
    
    try:
        db.session.add(novo_convidado)
        db.session.commit()
        flash(f'Presença confirmada com sucesso! Obrigado, {nome}!', 'success')
        return redirect(url_for('main.lista_presentes'))
    except Exception as e:
        db.session.rollback()
        flash('Erro ao confirmar presença. Tente novamente.', 'error')
        return redirect(url_for('main.local'))

@main.route('/presentes')
def lista_presentes():
    """Página da lista de presentes"""
    config = ConfiguracaoSite.query.first()
    presentes = Presente.query.filter_by(disponivel=True).all()
    
    return render_template('presentes.html', config=config, presentes=presentes)

@main.route('/confirmar-presenca')
def confirmar_presenca():
    """Página de confirmação de presença"""
    config = ConfiguracaoSite.query.first()
    
    # Calcular data limite para confirmação (30 dias antes do casamento)
    data_limite = None
    if config and config.data_casamento:
        from datetime import timedelta
        data_limite = config.data_casamento - timedelta(days=30)
    
    return render_template('confirmar_presenca.html', config=config, data_limite=data_limite)

@main.route('/convite-recepcao')
def convite_recepcao():
    """Página do convite de recepção - apenas para quem confirmou presença"""
    config = ConfiguracaoSite.query.first()
    if not config:
        # Criar configuração padrão se não existir
        config = ConfiguracaoSite(
            nome_noiva='Iara',
            nome_noivo='Samuel',
            data_casamento=datetime(2025, 11, 8).date(),
            local_cerimonia='Igreja Nossa Senhora das Graças',
            endereco_cerimonia='Rua Domingos Alcíno Dadalto, 114, Jardim Itapemirim, Cachoeiro de Itapemirim - ES',
            horario_cerimonia=datetime.strptime('19:00', '%H:%M').time(),
            local_festa='Espaço Jardim Encantado',
            endereco_festa='Av. Paulista, 456 - Bela Vista, São Paulo - SP',
            horario_festa=datetime.strptime('20:00', '%H:%M').time(),
        )
        db.session.add(config)
        db.session.commit()
    
    return render_template('convite_recepcao.html', config=config)

@main.route('/escolher-presente', methods=['POST'])
def escolher_presente():
    """Processar escolha de presente via AJAX"""
    try:
        presente_id = request.form.get('presente_id')
        nome_presenteador = request.form.get('nome_presenteador')
        email_presenteador = request.form.get('email_presenteador')
        telefone_presenteador = request.form.get('telefone_presenteador')
        mensagem = request.form.get('mensagem', '')
        
        presente = Presente.query.get_or_404(presente_id)
        
        if not presente.disponivel:
            return jsonify({'success': False, 'message': 'Este presente já foi escolhido.'})
        
        # Verificar se o convidado já existe
        convidado = Convidado.query.filter_by(email=email_presenteador).first()
        
        if not convidado:
            # Criar novo convidado
            import uuid
            token = str(uuid.uuid4())
            
            convidado = Convidado(
                nome=nome_presenteador,
                email=email_presenteador,
                telefone=telefone_presenteador,
                token=token
            )
            db.session.add(convidado)
            db.session.flush()  # Para obter o ID
        
        # Criar escolha do presente
        escolha = EscolhaPresente(
            convidado_id=convidado.id,
            presente_id=presente.id,
            nome_presenteador=nome_presenteador,
            email_presenteador=email_presenteador,
            telefone_presenteador=telefone_presenteador,
            mensagem=mensagem,
            data_escolha=datetime.utcnow()
        )
        
        # Marcar presente como não disponível
        presente.disponivel = False
        
        db.session.add(escolha)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'Presente "{presente.nome}" escolhido com sucesso!',
            'presente_id': presente.id
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Erro ao escolher presente. Tente novamente.'})

@main.route('/api/presentes')
def api_presentes():
    """API para buscar presentes disponíveis"""
    presentes = Presente.query.filter_by(disponivel=True).all()
    
    return jsonify([{
        'id': p.id,
        'nome': p.nome,
        'descricao': p.descricao,
        'categoria': p.categoria,
        'preco_sugerido': float(p.preco_sugerido) if p.preco_sugerido else None,
        'foi_escolhido': p.foi_escolhido,
        'imagem_url': p.imagem_url
    } for p in presentes])

@main.route('/teste-presentes')
def teste_presentes():
    """Página de teste para verificar se os presentes estão carregando"""
    return render_template('teste_presentes_simples.html')

@main.route('/init-data')
def init_data():
    """Inicializar dados de exemplo (apenas desenvolvimento)"""
    # Verificar se já existem presentes
    if Presente.query.count() > 0:
        flash('Dados já foram inicializados.', 'info')
        return redirect(url_for('main.index'))
    
    # Criar presentes de exemplo
    presentes = [
        {
            'nome': 'Jogo de Panelas Antiaderente',
            'descricao': 'Conjunto com 5 panelas antiaderentes de alta qualidade',
            'categoria': 'cozinha',
            'preco_sugerido': 299.90,
            'disponivel': True
        },
        {
            'nome': 'Conjunto de Taças de Cristal',
            'descricao': 'Kit com 6 taças de cristal para vinho e champanhe',
            'categoria': 'casa',
            'preco_sugerido': 189.90,
            'disponivel': True
        },
        {
            'nome': 'Jogo de Cama King Size',
            'descricao': 'Jogo de cama 100% algodão, 4 peças, king size',
            'categoria': 'quarto',
            'preco_sugerido': 159.90,
            'disponivel': True
        },
        {
            'nome': 'Cafeteira Elétrica',
            'descricao': 'Cafeteira elétrica programável para 12 xícaras',
            'categoria': 'cozinha',
            'preco_sugerido': 149.90,
            'disponivel': True
        },
        {
            'nome': 'Conjunto de Almofadas Decorativas',
            'descricao': 'Kit com 4 almofadas decorativas para sala',
            'categoria': 'sala',
            'preco_sugerido': 79.90,
            'disponivel': True
        },
        {
            'nome': 'Jantar Romântico para Dois',
            'descricao': 'Vale para jantar romântico em restaurante especial',
            'categoria': 'experiencias',
            'preco_sugerido': 250.00,
            'disponivel': True
        },
        {
            'nome': 'Aparelho de Jantar 20 Peças',
            'descricao': 'Aparelho de jantar em porcelana, 20 peças',
            'categoria': 'casa',
            'preco_sugerido': 199.90,
            'disponivel': True
        },
        {
            'nome': 'Liquidificador High Power',
            'descricao': 'Liquidificador de alta potência com 12 velocidades',
            'categoria': 'cozinha',
            'preco_sugerido': 179.90,
            'disponivel': True
        }
    ]
    
    for presente_data in presentes:
        presente = Presente(**presente_data)
        db.session.add(presente)
    
    db.session.commit()
    
    flash(f'{len(presentes)} presentes adicionados com sucesso!', 'success')
    return redirect(url_for('main.lista_presentes'))
