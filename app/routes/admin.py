from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, Admin, ConfiguracaoSite, Convidado, Presente, EscolhaPresente
from app import login_manager
from datetime import datetime

admin = Blueprint('admin', __name__)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

@admin.route('/login')
def login():
    """Página de login do administrador"""
    return render_template('admin/login.html')

@admin.route('/login', methods=['POST'])
def process_login():
    """Processar login do administrador"""
    username = request.form.get('username')
    password = request.form.get('password')
    
    user = Admin.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        login_user(user)
        flash('Login realizado com sucesso!', 'success')
        return redirect(url_for('admin.dashboard'))
    else:
        flash('Usuário ou senha inválidos.', 'error')
        return redirect(url_for('admin.login'))

@admin.route('/logout')
@login_required
def logout():
    """Logout do administrador"""
    logout_user()
    flash('Logout realizado com sucesso.', 'info')
    return redirect(url_for('main.index'))

@admin.route('/')
@admin.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal do administrador"""
    # Estatísticas gerais
    total_convidados = Convidado.query.count()
    confirmados = Convidado.query.filter_by(confirmou_presenca=True).count()
    liberados_recepcao = Convidado.query.filter_by(liberado_recepcao=True).count()
    total_presentes = Presente.query.count()
    presentes_escolhidos = EscolhaPresente.query.count()
    
    # Convidados recentes
    convidados_recentes = Convidado.query.order_by(Convidado.created_at.desc()).limit(5).all()
    
    # Convidados liberados para recepção
    convidados_liberados = Convidado.query.filter_by(liberado_recepcao=True).order_by(Convidado.data_confirmacao.desc()).limit(10).all()
    
    # Presentes mais populares
    presentes_populares = db.session.query(
        Presente, db.func.count(EscolhaPresente.id).label('escolhas')
    ).outerjoin(EscolhaPresente).group_by(Presente.id).order_by(db.text('escolhas DESC')).limit(5).all()
    
    config = ConfiguracaoSite.query.first()
    
    stats = {
        'total_convidados': total_convidados,
        'confirmados': confirmados,
        'liberados_recepcao': liberados_recepcao,
        'total_presentes': total_presentes,
        'presentes_escolhidos': presentes_escolhidos,
        'nao_confirmados': total_convidados - confirmados
    }
    
    return render_template('admin/dashboard.html', 
                         stats=stats, 
                         convidados_recentes=convidados_recentes,
                         convidados_liberados=convidados_liberados,
                         presentes_populares=presentes_populares,
                         config=config)

@admin.route('/convidados')
@login_required
def convidados():
    """Gerenciar convidados"""
    page = request.args.get('page', 1, type=int)
    convidados = Convidado.query.order_by(Convidado.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/convidados.html', convidados=convidados)

@admin.route('/convidados/adicionar')
@login_required
def adicionar_convidado():
    """Formulário para adicionar convidado"""
    return render_template('admin/adicionar_convidado.html')

@admin.route('/convidados/adicionar', methods=['POST'])
@login_required
def processar_adicionar_convidado():
    """Processar adição de convidado"""
    try:
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        
        # Gerar token único
        import uuid
        token = str(uuid.uuid4())
        
        convidado = Convidado(
            nome=nome,
            email=email,
            telefone=telefone,
            token=token
        )
        
        db.session.add(convidado)
        db.session.commit()
        
        flash(f'Convidado {nome} adicionado com sucesso!', 'success')
        return redirect(url_for('admin.convidados'))
        
    except Exception as e:
        flash('Erro ao adicionar convidado. Tente novamente.', 'error')
        return redirect(url_for('admin.adicionar_convidado'))

@admin.route('/presentes')
@login_required
def presentes():
    """Gerenciar presentes"""
    page = request.args.get('page', 1, type=int)
    presentes = Presente.query.order_by(Presente.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/presentes.html', presentes=presentes)

@admin.route('/presentes/adicionar')
@login_required
def adicionar_presente():
    """Formulário para adicionar presente"""
    return render_template('admin/adicionar_presente.html')

@admin.route('/presentes/adicionar', methods=['POST'])
@login_required
def processar_adicionar_presente():
    """Processar adição de presente"""
    try:
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        categoria = request.form.get('categoria')
        preco_sugerido = request.form.get('preco_sugerido')
        link_loja = request.form.get('link_loja')
        imagem_url = request.form.get('imagem_url')
        
        presente = Presente(
            nome=nome,
            descricao=descricao,
            categoria=categoria,
            preco_sugerido=float(preco_sugerido) if preco_sugerido else None,
            link_loja=link_loja,
            imagem_url=imagem_url
        )
        
        db.session.add(presente)
        db.session.commit()
        
        flash(f'Presente "{nome}" adicionado com sucesso!', 'success')
        return redirect(url_for('admin.presentes'))
        
    except Exception as e:
        flash('Erro ao adicionar presente. Tente novamente.', 'error')
        return redirect(url_for('admin.adicionar_presente'))

@admin.route('/configuracoes')
@login_required
def configuracoes():
    """Configurações do site"""
    config = ConfiguracaoSite.query.first()
    if not config:
        config = ConfiguracaoSite()
        db.session.add(config)
        db.session.commit()
    
    return render_template('admin/configuracoes.html', config=config)

@admin.route('/configuracoes', methods=['POST'])
@login_required
def processar_configuracoes():
    """Processar alterações de configuração"""
    try:
        config = ConfiguracaoSite.query.first()
        if not config:
            config = ConfiguracaoSite()
        
        config.nome_noiva = request.form.get('nome_noiva')
        config.nome_noivo = request.form.get('nome_noivo')
        
        # Converter data
        data_str = request.form.get('data_casamento')
        if data_str:
            config.data_casamento = datetime.strptime(data_str, '%Y-%m-%d').date()
        
        config.local_cerimonia = request.form.get('local_cerimonia')
        config.endereco_cerimonia = request.form.get('endereco_cerimonia')
        config.local_festa = request.form.get('local_festa')
        config.endereco_festa = request.form.get('endereco_festa')
        config.mensagem_principal = request.form.get('mensagem_principal')
        config.cor_tema = request.form.get('cor_tema')
        
        db.session.add(config)
        db.session.commit()
        
        flash('Configurações atualizadas com sucesso!', 'success')
        return redirect(url_for('admin.configuracoes'))
        
    except Exception as e:
        flash('Erro ao atualizar configurações. Tente novamente.', 'error')
        return redirect(url_for('admin.configuracoes'))
