from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models import db, ConfiguracaoSite, Convidado, Presente, EscolhaPresente
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Página principal do convite"""
    config = ConfiguracaoSite.query.first()
    if not config:
        # Criar configuração padrão se não existir
        config = ConfiguracaoSite(
            nome_noiva='Iara',
            nome_noivo='Samuel',
            data_casamento=datetime(2025, 11, 28).date(),
            local_cerimonia='Igreja São Francisco de Assis',
            endereco_cerimonia='Rua das Flores, 123 - Centro, São Paulo - SP',
            horario_cerimonia=datetime.strptime('16:00', '%H:%M').time(),
            local_festa='Espaço Jardim Encantado',
            endereco_festa='Av. Paulista, 456 - Bela Vista, São Paulo - SP',
            horario_festa=datetime.strptime('18:00', '%H:%M').time(),
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
    return render_template('confirmar_presenca.html', config=config)

@main.route('/confirmar-presenca', methods=['POST'])
def processar_confirmacao():
    """Processar confirmação de presença"""
    try:
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        acompanhantes = int(request.form.get('acompanhantes', 0))
        observacoes = request.form.get('observacoes')
        
        # Gerar token único
        import uuid
        token = str(uuid.uuid4())
        
        # Criar novo convidado
        convidado = Convidado(
            nome=nome,
            email=email,
            telefone=telefone,
            token=token,
            confirmou_presenca=True,
            data_confirmacao=datetime.utcnow(),
            acompanhantes=acompanhantes,
            observacoes=observacoes
        )
        
        db.session.add(convidado)
        db.session.commit()
        
        flash('Presença confirmada com sucesso! Obrigado por confirmar.', 'success')
        return redirect(url_for('main.presentes'))
        
    except Exception as e:
        flash('Erro ao confirmar presença. Tente novamente.', 'error')
        return redirect(url_for('main.confirmar_presenca'))

@main.route('/escolher-presente/<int:presente_id>')
def escolher_presente(presente_id):
    """Escolher um presente da lista"""
    presente = Presente.query.get_or_404(presente_id)
    
    if presente.foi_escolhido:
        flash('Este presente já foi escolhido por outro convidado.', 'warning')
        return redirect(url_for('main.lista_presentes'))
    
    return render_template('escolher_presente.html', presente=presente)

@main.route('/escolher-presente/<int:presente_id>', methods=['POST'])
def processar_escolha_presente(presente_id):
    """Processar escolha de presente"""
    try:
        presente = Presente.query.get_or_404(presente_id)
        
        if presente.foi_escolhido:
            flash('Este presente já foi escolhido por outro convidado.', 'warning')
            return redirect(url_for('main.lista_presentes'))
        
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        
        # Verificar se o convidado já existe
        convidado = Convidado.query.filter_by(email=email).first()
        
        if not convidado:
            # Criar novo convidado
            import uuid
            token = str(uuid.uuid4())
            
            convidado = Convidado(
                nome=nome,
                email=email,
                telefone=telefone,
                token=token
            )
            db.session.add(convidado)
            db.session.flush()  # Para obter o ID
        
        # Criar escolha do presente
        escolha = EscolhaPresente(
            convidado_id=convidado.id,
            presente_id=presente.id
        )
        
        db.session.add(escolha)
        db.session.commit()
        
        flash(f'Presente "{presente.nome}" reservado com sucesso! Obrigado.', 'success')
        return redirect(url_for('main.lista_presentes'))
        
    except Exception as e:
        flash('Erro ao escolher presente. Tente novamente.', 'error')
        return redirect(url_for('main.lista_presentes'))

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
