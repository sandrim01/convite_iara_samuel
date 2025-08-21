from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, Admin, ConfiguracaoSite, Convidado, Presente, EscolhaPresente
from app import login_manager
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from PIL import Image
from io import BytesIO

admin = Blueprint('admin', __name__)

# Configurações para upload de imagens
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    """Verifica se o arquivo tem uma extensão permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image(file):
    """Processa a imagem para otimização"""
    try:
        # Abrir imagem
        image = Image.open(file.stream)
        
        # Converter para RGB se necessário
        if image.mode in ('RGBA', 'P'):
            image = image.convert('RGB')
        
        # Redimensionar se muito grande
        max_size = (800, 600)
        if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Salvar em buffer
        buffer = BytesIO()
        image.save(buffer, format='JPEG', quality=85, optimize=True)
        buffer.seek(0)
        
        return buffer
        
    except Exception as e:
        raise ValueError(f"Erro ao processar imagem: {str(e)}")

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

@admin.route('/login')
def login():
    """Página de login do administrador"""
    config = ConfiguracaoSite.query.first()
    return render_template('admin/login.html', config=config)

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
    confirmados = Convidado.query.filter_by(confirmacao=True).count()
    liberados_recepcao = Convidado.query.filter_by(liberado_recepcao=True).count()
    total_presentes = Presente.query.count()
    presentes_escolhidos = EscolhaPresente.query.count()
    
    # Convidados recentes
    convidados_recentes = Convidado.query.order_by(Convidado.created_at.desc()).limit(5).all()
    
    # Confirmações recentes
    confirmacoes_recentes = Convidado.query.filter_by(confirmacao=True).order_by(Convidado.data_confirmacao.desc()).limit(5).all()
    
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
                         confirmacoes_recentes=confirmacoes_recentes,
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

@admin.route('/presentes/<int:id>/editar')
@login_required
def editar_presente(id):
    """Formulário para editar presente"""
    presente = Presente.query.get_or_404(id)
    return render_template('admin/editar_presente.html', presente=presente)

@admin.route('/presentes/<int:id>/editar', methods=['POST'])
@login_required
def processar_editar_presente(id):
    """Processar edição de presente"""
    try:
        presente = Presente.query.get_or_404(id)
        
        presente.nome = request.form.get('nome')
        presente.descricao = request.form.get('descricao')
        presente.categoria = request.form.get('categoria')
        
        preco_sugerido = request.form.get('preco_sugerido')
        presente.preco_sugerido = float(preco_sugerido) if preco_sugerido else None
        
        presente.link_loja = request.form.get('link_loja')
        presente.imagem_url = request.form.get('imagem_url')
        
        db.session.commit()
        
        flash(f'Presente "{presente.nome}" atualizado com sucesso!', 'success')
        return redirect(url_for('admin.presentes'))
        
    except Exception as e:
        flash('Erro ao atualizar presente. Tente novamente.', 'error')
        return redirect(url_for('admin.editar_presente', id=id))

@admin.route('/presentes/<int:id>/remover', methods=['POST'])
@login_required
def remover_presente(id):
    """Remover presente"""
    try:
        presente = Presente.query.get_or_404(id)
        nome = presente.nome
        
        # Verificar se o presente já foi escolhido
        escolhas = EscolhaPresente.query.filter_by(presente_id=id).count()
        if escolhas > 0:
            flash(f'Não é possível remover o presente "{nome}" pois já foi escolhido por {escolhas} pessoa(s).', 'error')
            return redirect(url_for('admin.presentes'))
        
        db.session.delete(presente)
        db.session.commit()
        
        flash(f'Presente "{nome}" removido com sucesso!', 'success')
        return redirect(url_for('admin.presentes'))
        
    except Exception as e:
        flash('Erro ao remover presente. Tente novamente.', 'error')
        return redirect(url_for('admin.presentes'))

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
        
        # Dados básicos do casal
        config.nome_noiva = request.form.get('nome_noiva')
        config.nome_noivo = request.form.get('nome_noivo')
        
        # Converter data
        data_str = request.form.get('data_casamento')
        if data_str:
            config.data_casamento = datetime.strptime(data_str, '%Y-%m-%d').date()
        
        # Converter horários
        horario_cerimonia_str = request.form.get('horario_cerimonia')
        if horario_cerimonia_str:
            config.horario_cerimonia = datetime.strptime(horario_cerimonia_str, '%H:%M').time()
            
        horario_festa_str = request.form.get('horario_festa')
        if horario_festa_str:
            config.horario_festa = datetime.strptime(horario_festa_str, '%H:%M').time()
        
        # Locais e endereços
        config.local_cerimonia = request.form.get('local_cerimonia')
        config.endereco_cerimonia = request.form.get('endereco_cerimonia')
        config.local_festa = request.form.get('local_festa')
        config.endereco_festa = request.form.get('endereco_festa')
        
        # Personalização
        config.mensagem_principal = request.form.get('mensagem_principal')
        config.cor_tema = request.form.get('cor_tema')
        config.foto_casal = request.form.get('foto_casal')
        
        # Informações da noiva
        config.descricao_noiva = request.form.get('descricao_noiva')
        config.aniversario_noiva = request.form.get('aniversario_noiva')
        config.paixoes_noiva = request.form.get('paixoes_noiva')
        config.frase_noiva = request.form.get('frase_noiva')
        config.foto_noiva = request.form.get('foto_noiva')
        
        # Informações do noivo
        config.descricao_noivo = request.form.get('descricao_noivo')
        config.aniversario_noivo = request.form.get('aniversario_noivo')
        config.paixoes_noivo = request.form.get('paixoes_noivo')
        config.frase_noivo = request.form.get('frase_noivo')
        config.foto_noivo = request.form.get('foto_noivo')
        
        # História de amor - checkbox
        config.mostrar_historia = 'mostrar_historia' in request.form
        
        # Timeline da história
        if config.mostrar_historia:
            config.primeiro_encontro_ano = request.form.get('primeiro_encontro_ano')
            config.primeiro_encontro_texto = request.form.get('primeiro_encontro_texto')
            config.namoro_ano = request.form.get('namoro_ano')
            config.namoro_texto = request.form.get('namoro_texto')
            config.pedido_ano = request.form.get('pedido_ano')
            config.pedido_texto = request.form.get('pedido_texto')
            config.grande_dia_ano = request.form.get('grande_dia_ano')
            config.grande_dia_texto = request.form.get('grande_dia_texto')
        
        db.session.add(config)
        db.session.commit()
        
        flash('Configurações atualizadas com sucesso!', 'success')
        return redirect(url_for('admin.dashboard'))
        
    except Exception as e:
        flash('Erro ao atualizar configurações. Tente novamente.', 'error')
        return redirect(url_for('admin.dashboard'))

@admin.route('/upload-foto', methods=['POST'])
@login_required
def upload_foto():
    """Upload de fotos dos noivos"""
    try:
        if 'foto' not in request.files:
            return jsonify({'success': False, 'error': 'Nenhum arquivo enviado'})
        
        file = request.files['foto']
        tipo = request.form.get('tipo')  # casal, noiva, noivo
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'Nenhum arquivo selecionado'})
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Tipo de arquivo não permitido'})
        
        if not tipo or tipo not in ['casal', 'noiva', 'noivo']:
            return jsonify({'success': False, 'error': 'Tipo de foto inválido'})
        
        # Processar a imagem
        try:
            processed_image = process_image(file)
            filename = secure_filename(file.filename)
            
            # Salvar no banco de dados
            config = ConfiguracaoSite.query.first()
            if not config:
                config = ConfiguracaoSite()
                db.session.add(config)
            
            # Determinar qual campo atualizar
            blob_field = f'foto_{tipo}_blob'
            filename_field = f'foto_{tipo}_filename'
            mimetype_field = f'foto_{tipo}_mimetype'
            
            setattr(config, blob_field, processed_image.getvalue())
            setattr(config, filename_field, filename)
            setattr(config, mimetype_field, file.mimetype)
            
            db.session.commit()
            
            # Retornar URL da imagem
            image_url = url_for('main.serve_image', tipo=tipo, id=config.id)
            
            return jsonify({
                'success': True,
                'url': image_url,
                'message': 'Foto enviada com sucesso!'
            })
            
        except Exception as e:
            return jsonify({'success': False, 'error': f'Erro ao processar imagem: {str(e)}'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Erro interno: {str(e)}'})

@admin.route('/teste-upload-foto', methods=['POST'])
def teste_upload_foto():
    """Versão de teste do upload (sem autenticação)"""
    try:
        if 'foto' not in request.files:
            return jsonify({'success': False, 'error': 'Nenhum arquivo enviado'})
        
        file = request.files['foto']
        tipo = request.form.get('tipo')  # casal, noiva, noivo
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'Nenhum arquivo selecionado'})
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Tipo de arquivo não permitido'})
        
        if not tipo or tipo not in ['casal', 'noiva', 'noivo']:
            return jsonify({'success': False, 'error': 'Tipo de foto inválido'})
        
        # Processar a imagem
        try:
            processed_image = process_image(file)
            filename = secure_filename(file.filename)
            
            # Salvar no banco de dados
            config = ConfiguracaoSite.query.first()
            if not config:
                config = ConfiguracaoSite()
                db.session.add(config)
            
            # Determinar qual campo atualizar
            blob_field = f'foto_{tipo}_blob'
            filename_field = f'foto_{tipo}_filename'
            mimetype_field = f'foto_{tipo}_mimetype'
            
            setattr(config, blob_field, processed_image.getvalue())
            setattr(config, filename_field, filename)
            setattr(config, mimetype_field, file.mimetype)
            
            db.session.commit()
            
            # Retornar URL da imagem
            image_url = url_for('main.serve_image', tipo=tipo, id=config.id)
            
            return jsonify({
                'success': True,
                'url': image_url,
                'message': 'Foto enviada com sucesso! (modo teste)'
            })
            
        except Exception as e:
            return jsonify({'success': False, 'error': f'Erro ao processar imagem: {str(e)}'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Erro interno: {str(e)}'})
