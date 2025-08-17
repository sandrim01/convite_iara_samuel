from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, login_user, logout_user, current_user
from app.models import Admin, Convidado, Presente, EscolhaPresente, ConfiguracaoSite
from app import db
from werkzeug.security import generate_password_hash
from datetime import datetime

admin = Blueprint('admin', __name__)

@admin.route('/login', methods=['GET', 'POST'])
def login():
    """Login do administrador"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = Admin.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Usuário ou senha incorretos!', 'error')
    
    return render_template('admin/login.html')

@admin.route('/logout')
@login_required
def logout():
    """Logout do administrador"""
    logout_user()
    return redirect(url_for('main.index'))

@admin.route('/dashboard')
@login_required
def dashboard():
    """Dashboard administrativo"""
    total_convidados = Convidado.query.count()
    confirmados = Convidado.query.filter_by(confirmou_presenca=True).count()
    total_presentes = Presente.query.count()
    presentes_escolhidos = EscolhaPresente.query.count()
    
    stats = {
        'total_convidados': total_convidados,
        'confirmados': confirmados,
        'total_presentes': total_presentes,
        'presentes_escolhidos': presentes_escolhidos
    }
    
    return render_template('admin/dashboard.html', stats=stats)

@admin.route('/convidados')
@login_required
def convidados():
    """Gerenciar convidados"""
    convidados = Convidado.query.all()
    return render_template('admin/convidados.html', convidados=convidados)

@admin.route('/convidados/add', methods=['GET', 'POST'])
@login_required
def add_convidado():
    """Adicionar novo convidado"""
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        
        convidado = Convidado(
            nome=nome,
            email=email,
            telefone=telefone
        )
        
        db.session.add(convidado)
        db.session.commit()
        
        flash(f'Convidado {nome} adicionado com sucesso!', 'success')
        return redirect(url_for('admin.convidados'))
    
    return render_template('admin/add_convidado.html')

@admin.route('/presentes')
@login_required
def presentes():
    """Gerenciar presentes"""
    presentes = Presente.query.all()
    return render_template('admin/presentes.html', presentes=presentes)

@admin.route('/presentes/add', methods=['GET', 'POST'])
@login_required
def add_presente():
    """Adicionar novo presente"""
    if request.method == 'POST':
        nome = request.form['nome']
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
        
        flash(f'Presente {nome} adicionado com sucesso!', 'success')
        return redirect(url_for('admin.presentes'))
    
    return render_template('admin/add_presente.html')

@admin.route('/configuracoes', methods=['GET', 'POST'])
@login_required
def configuracoes():
    """Configurações do site"""
    config = ConfiguracaoSite.query.first()
    if not config:
        config = ConfiguracaoSite()
        db.session.add(config)
        db.session.commit()
    
    if request.method == 'POST':
        config.nome_noiva = request.form['nome_noiva']
        config.nome_noivo = request.form['nome_noivo']
        config.mensagem_principal = request.form['mensagem_principal']
        config.local_cerimonia = request.form.get('local_cerimonia')
        config.endereco_cerimonia = request.form.get('endereco_cerimonia')
        config.local_festa = request.form.get('local_festa')
        config.endereco_festa = request.form.get('endereco_festa')
        config.cor_tema = request.form.get('cor_tema', '#ff69b4')
        
        # Tratar data do casamento
        data_casamento = request.form.get('data_casamento')
        if data_casamento:
            config.data_casamento = datetime.strptime(data_casamento, '%Y-%m-%d').date()
        
        config.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash('Configurações salvas com sucesso!', 'success')
        return redirect(url_for('admin.configuracoes'))
    
    return render_template('admin/configuracoes.html', config=config)

@admin.route('/setup', methods=['GET', 'POST'])
def setup():
    """Configuração inicial do administrador"""
    # Verificar se já existe um admin
    if Admin.query.first():
        return redirect(url_for('admin.login'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        admin_user = Admin(
            username=username,
            email=email
        )
        admin_user.set_password(password)
        
        db.session.add(admin_user)
        db.session.commit()
        
        flash('Administrador criado com sucesso! Faça login.', 'success')
        return redirect(url_for('admin.login'))
    
    return render_template('admin/setup.html')
