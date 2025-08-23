from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, Admin, ConfiguracaoSite, Convidado, Presente, EscolhaPresente
from app import login_manager
from datetime import datetime
import os
import re
import requests
from werkzeug.utils import secure_filename
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup

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
    
    # Cálculos de pessoas (convidados + acompanhantes)
    # Total de pessoas confirmadas (soma dos acompanhantes dos confirmados + os próprios convidados confirmados)
    convidados_confirmados = Convidado.query.filter_by(confirmacao=True).all()
    total_pessoas = sum(1 + (c.numero_acompanhantes or 0) for c in convidados_confirmados)
    pessoas_cerimonia = total_pessoas  # Todos os confirmados vão à cerimônia
    
    # Pessoas na recepção (apenas os liberados para recepção)
    convidados_recepcao = Convidado.query.filter_by(confirmacao=True, liberado_recepcao=True).all()
    pessoas_recepcao = sum(1 + (c.numero_acompanhantes or 0) for c in convidados_recepcao)
    
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
        'nao_confirmados': total_convidados - confirmados,
        'total_pessoas': total_pessoas,
        'pessoas_cerimonia': pessoas_cerimonia,
        'pessoas_recepcao': pessoas_recepcao
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
    print(f"🗑️  Tentativa de remoção do presente ID: {id}")
    try:
        presente = Presente.query.get_or_404(id)
        nome = presente.nome
        print(f"📋 Presente encontrado: '{nome}'")
        
        # Verificar se o presente já foi escolhido
        escolhas = EscolhaPresente.query.filter_by(presente_id=id).count()
        print(f"📊 Escolhas encontradas: {escolhas}")
        
        if escolhas > 0:
            print(f"❌ Presente não pode ser removido - já foi escolhido {escolhas} vez(es)")
            flash(f'Não é possível remover o presente "{nome}" pois já foi escolhido por {escolhas} pessoa(s).', 'error')
            return redirect(url_for('admin.presentes'))
        
        print(f"✅ Removendo presente '{nome}'")
        db.session.delete(presente)
        db.session.commit()
        
        print(f"🎉 Presente '{nome}' removido com sucesso!")
        flash(f'Presente "{nome}" removido com sucesso!', 'success')
        return redirect(url_for('admin.presentes'))
        
    except Exception as e:
        print(f"💥 Erro ao remover presente: {str(e)}")
        flash('Erro ao remover presente. Tente novamente.', 'error')
        return redirect(url_for('admin.presentes'))

@admin.route('/presentes/<int:id>')
@login_required
def obter_presente(id):
    """Obter dados de um presente específico"""
    try:
        presente = Presente.query.get_or_404(id)
        return jsonify({
            'id': presente.id,
            'nome': presente.nome,
            'preco': float(presente.preco),
            'imagem_url': presente.imagem_url,
            'escolhido': presente.escolhido
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

        # Upload de fotos do modal (Visual & Tema)
        # Foto do Casal
        file_casal = request.files.get('foto_casal_modal')
        if file_casal and file_casal.filename:
            config.foto_casal_blob = file_casal.read()
            config.foto_casal_filename = file_casal.filename
            config.foto_casal_mimetype = file_casal.mimetype

        # Foto da Noiva
        file_noiva = request.files.get('foto_noiva_modal')
        if file_noiva and file_noiva.filename:
            config.foto_noiva_blob = file_noiva.read()
            config.foto_noiva_filename = file_noiva.filename
            config.foto_noiva_mimetype = file_noiva.mimetype

        # Foto do Noivo
        file_noivo = request.files.get('foto_noivo_modal')
        if file_noivo and file_noivo.filename:
            config.foto_noivo_blob = file_noivo.read()
            config.foto_noivo_filename = file_noivo.filename
            config.foto_noivo_mimetype = file_noivo.mimetype
        
        # Informações da noiva
        config.descricao_noiva = request.form.get('descricao_noiva')
        config.aniversario_noiva = request.form.get('aniversario_noiva')
        config.paixoes_noiva = request.form.get('paixoes_noiva')
        config.frase_noiva = request.form.get('frase_noiva')
    # O campo config.foto_noiva (string) não é mais usado, pois agora é BLOB
        
        # Informações do noivo
        config.descricao_noivo = request.form.get('descricao_noivo')
        config.aniversario_noivo = request.form.get('aniversario_noivo')
        config.paixoes_noivo = request.form.get('paixoes_noivo')
        config.frase_noivo = request.form.get('frase_noivo')
    # O campo config.foto_noivo (string) não é mais usado, pois agora é BLOB
        
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

# ===== ROTAS PARA GERENCIAMENTO DE CONVIDADOS =====

@admin.route('/api/stats')
@login_required
def api_stats():
    """API para atualizar estatísticas do dashboard"""
    try:
        # Estatísticas gerais
        total_convidados = Convidado.query.count()
        confirmados = Convidado.query.filter_by(confirmacao=True).count()
        liberados_recepcao = Convidado.query.filter_by(liberado_recepcao=True).count()
        presentes_escolhidos = EscolhaPresente.query.count()
        
        # Cálculos de pessoas (convidados + acompanhantes)
        convidados_confirmados = Convidado.query.filter_by(confirmacao=True).all()
        total_pessoas = sum(1 + (c.numero_acompanhantes or 0) for c in convidados_confirmados)
        pessoas_cerimonia = total_pessoas
        
        convidados_recepcao = Convidado.query.filter_by(confirmacao=True, liberado_recepcao=True).all()
        pessoas_recepcao = sum(1 + (c.numero_acompanhantes or 0) for c in convidados_recepcao)
        
        return jsonify({
            'total_convidados': total_convidados,
            'confirmados': confirmados,
            'liberados_recepcao': liberados_recepcao,
            'nao_confirmados': total_convidados - confirmados,
            'presentes_escolhidos': presentes_escolhidos,
            'total_pessoas': total_pessoas,
            'pessoas_cerimonia': pessoas_cerimonia,
            'pessoas_recepcao': pessoas_recepcao
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/convidados')
@login_required
def api_convidados():
    """API para carregar convidados no modal"""
    try:
        # Buscar todos os convidados
        convidados = Convidado.query.order_by(Convidado.created_at.desc()).all()
        
        # Calcular estatísticas
        total = len(convidados)
        confirmados = len([c for c in convidados if c.confirmacao])
        pendentes = total - confirmados
        liberados = len([c for c in convidados if c.liberado_recepcao])
        
        # Converter para formato JSON
        convidados_data = []
        for convidado in convidados:
            convidados_data.append({
                'id': convidado.id,
                'nome': convidado.nome,
                'email': convidado.email,
                'telefone': convidado.telefone,
                'token': convidado.token,
                'confirmacao': convidado.confirmacao,
                'numero_acompanhantes': convidado.numero_acompanhantes or 0,
                'liberado_recepcao': convidado.liberado_recepcao,
                'data_confirmacao': convidado.data_confirmacao.isoformat() if convidado.data_confirmacao else None
            })
        
        return jsonify({
            'success': True,
            'convidados': convidados_data,
            'stats': {
                'total': total,
                'confirmados': confirmados,
                'pendentes': pendentes,
                'liberados': liberados
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao carregar convidados: {str(e)}'
        })

@admin.route('/convidados/<int:id>/toggle-recepcao', methods=['POST'])
@login_required
def toggle_recepcao_convidado(id):
    """Toggle liberação para recepção do convidado"""
    try:
        convidado = Convidado.query.get_or_404(id)
        data = request.get_json()
        
        convidado.liberado_recepcao = data.get('enabled', False)
        db.session.commit()
        
        status = "liberado" if convidado.liberado_recepcao else "bloqueado"
        
        return jsonify({
            'success': True,
            'message': f'Convidado {status} para recepção'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao atualizar: {str(e)}'
        })

@admin.route('/convidados/<int:id>/detalhes')
@login_required
def detalhes_convidado(id):
    """Obter detalhes completos do convidado"""
    try:
        convidado = Convidado.query.get_or_404(id)
        
        return jsonify({
            'success': True,
            'guest': {
                'id': convidado.id,
                'nome': convidado.nome,
                'email': convidado.email,
                'telefone': convidado.telefone,
                'token': convidado.token,
                'confirmacao': convidado.confirmacao,
                'numero_acompanhantes': convidado.numero_acompanhantes,
                'liberado_recepcao': convidado.liberado_recepcao,
                'mensagem': convidado.mensagem,
                'data_confirmacao': convidado.data_confirmacao.isoformat() if convidado.data_confirmacao else None,
                'created_at': convidado.created_at.isoformat() if hasattr(convidado, 'created_at') and convidado.created_at else None
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao carregar detalhes: {str(e)}'
        })

@admin.route('/convidados/<int:id>/editar')
@login_required
def editar_convidado(id):
    """Formulário para editar convidado"""
    convidado = Convidado.query.get_or_404(id)
    return render_template('admin/editar_convidado.html', convidado=convidado)

@admin.route('/convidados/<int:id>/editar', methods=['POST'])
@login_required
def processar_editar_convidado(id):
    """Processar edição de convidado"""
    try:
        convidado = Convidado.query.get_or_404(id)
        
        convidado.nome = request.form.get('nome')
        convidado.email = request.form.get('email')
        convidado.telefone = request.form.get('telefone')
        convidado.liberado_recepcao = 'liberado_recepcao' in request.form
        
        db.session.commit()
        
        flash(f'Convidado "{convidado.nome}" atualizado com sucesso!', 'success')
        return redirect(url_for('admin.convidados'))
        
    except Exception as e:
        flash('Erro ao atualizar convidado. Tente novamente.', 'error')
        return redirect(url_for('admin.editar_convidado', id=id))

@admin.route('/convidados/<int:id>/excluir', methods=['DELETE'])
@login_required
def excluir_convidado(id):
    """Excluir convidado"""
    try:
        convidado = Convidado.query.get_or_404(id)
        nome = convidado.nome
        
        db.session.delete(convidado)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Convidado "{nome}" excluído com sucesso'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao excluir convidado: {str(e)}'
        })

@admin.route('/buscar-produto-por-link', methods=['POST'])
@login_required
def buscar_produto_por_link():
    """Busca informações de um produto através do link"""
    try:
        data = request.get_json()
        link = data.get('link', '').strip()
        
        if not link:
            return jsonify({'success': False, 'error': 'Link não fornecido'})
        
        # Aqui vamos implementar o scraping/busca das informações
        produto_info = extrair_informacoes_produto(link)
        
        if produto_info:
            return jsonify({
                'success': True,
                'nome': produto_info.get('nome'),
                'preco': produto_info.get('preco'),
                'descricao': produto_info.get('descricao'),
                'imagem': produto_info.get('imagem'),
                'link_original': link,
                'categoria': produto_info.get('categoria', 'casa')
            })
        else:
            return jsonify({'success': False, 'error': 'Não foi possível extrair informações do produto'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': f'Erro interno: {str(e)}'})

@admin.route('/adicionar-presente-por-link', methods=['POST'])
@login_required 
def adicionar_presente_por_link():
    """Adiciona um presente usando informações extraídas do link"""
    try:
        data = request.get_json()
        link = data.get('link', '').strip()
        
        if not link:
            return jsonify({'success': False, 'error': 'Link não fornecido'})
        
        # Extrair informações do produto
        print(f"🔍 Extraindo informações do link: {link}")
        info_produto = extrair_informacoes_produto(link)
        
        if not info_produto:
            return jsonify({'success': False, 'error': 'Não foi possível extrair informações do produto do link fornecido'})
        
        # Verificar se já existe um presente com esse link
        presente_existente = Presente.query.filter_by(link_loja=link).first()
        if presente_existente:
            return jsonify({'success': False, 'error': 'Este produto já foi adicionado à lista'})
        
        # Criar novo presente com as informações extraídas
        presente = Presente(
            nome=info_produto.get('nome', 'Produto sem nome'),
            preco=extrair_preco_numerico(info_produto.get('preco', '0')),
            imagem_url=info_produto.get('imagem', ''),
            link_loja=link,
            escolhido=False
        )
        
        db.session.add(presente)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Presente "{presente.nome}" adicionado com sucesso!',
            'presente_id': presente.id
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'Erro ao adicionar presente: {str(e)}'})

def extrair_informacoes_produto(link):
    """Extrai informações do produto a partir do link"""
    import requests
    from bs4 import BeautifulSoup
    import re
    
    try:
        # Headers para simular um navegador real
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        response = requests.get(link, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extrair informações com diferentes estratégias dependendo do site
        nome = extrair_nome_produto(soup, link)
        preco = extrair_preco_produto(soup, link)
        descricao = extrair_descricao_produto(soup, link)
        imagem = extrair_imagem_produto(soup, link)
        categoria = determinar_categoria(nome, descricao)
        
        return {
            'nome': nome,
            'preco': preco,
            'descricao': descricao,
            'imagem': imagem,
            'categoria': categoria
        }
        
    except Exception as e:
        print(f"Erro ao extrair informações do produto: {e}")
        return None

def extrair_nome_produto(soup, link):
    """Extrai o nome do produto"""
    selectors = [
        'h1#productTitle',  # Amazon
        'h1.ui-pdp-title',  # Mercado Livre
        'h1.product-title',  # Magazine Luiza
        'h1.title',
        'h1',
        '.product-name',
        '.product-title',
        '[data-testid="product-title"]',
        'meta[property="og:title"]'
    ]
    
    for selector in selectors:
        try:
            if selector.startswith('meta'):
                element = soup.select_one(selector)
                if element:
                    return element.get('content', '').strip()
            else:
                element = soup.select_one(selector)
                if element:
                    return element.get_text().strip()
        except:
            continue
    
    # Fallback para o título da página
    title = soup.find('title')
    if title:
        return title.get_text().strip()
    
    return 'Produto'

def extrair_preco_produto(soup, link):
    """Extrai o preço do produto"""
    selectors = [
        '.a-price-whole',  # Amazon
        '.andes-money-amount__fraction',  # Mercado Livre
        '.price-current',
        '.price',
        '.product-price',
        '[data-testid="price"]',
        'meta[property="product:price:amount"]'
    ]
    
    for selector in selectors:
        try:
            if selector.startswith('meta'):
                element = soup.select_one(selector)
                if element:
                    return f"R$ {element.get('content', '0')}"
            else:
                element = soup.select_one(selector)
                if element:
                    preco_text = element.get_text().strip()
                    # Procurar por padrões de preço
                    match = re.search(r'R?\$?\s*(\d+[,.]?\d*)', preco_text)
                    if match:
                        return f"R$ {match.group(1)}"
        except:
            continue
    
    return 'Consulte o site'

def extrair_descricao_produto(soup, link):
    """Extrai a descrição do produto"""
    selectors = [
        '#productDescription',  # Amazon
        '.ui-pdp-description',  # Mercado Livre
        '.product-description',
        '.description',
        'meta[property="og:description"]',
        'meta[name="description"]'
    ]
    
    for selector in selectors:
        try:
            if selector.startswith('meta'):
                element = soup.select_one(selector)
                if element:
                    desc = element.get('content', '').strip()
                    if len(desc) > 20:  # Evitar descrições muito curtas
                        return desc[:300] + '...' if len(desc) > 300 else desc
            else:
                element = soup.select_one(selector)
                if element:
                    desc = element.get_text().strip()
                    if len(desc) > 20:
                        return desc[:300] + '...' if len(desc) > 300 else desc
        except:
            continue
    
    return 'Descrição disponível no site da loja'

def extrair_imagem_produto(soup, link):
    """Extrai a imagem do produto"""
    selectors = [
        '#landingImage',  # Amazon
        '.ui-pdp-image',  # Mercado Livre
        '.product-image img',
        '.main-image img',
        'meta[property="og:image"]',
        'img[alt*="produto"], img[alt*="product"]'
    ]
    
    for selector in selectors:
        try:
            if selector.startswith('meta'):
                element = soup.select_one(selector)
                if element:
                    return element.get('content', '')
            else:
                element = soup.select_one(selector)
                if element:
                    src = element.get('src') or element.get('data-src')
                    if src and src.startswith('http'):
                        return src
        except:
            continue
    
    return ''

def determinar_categoria(nome, descricao):
    """Determina a categoria baseada no nome e descrição"""
    texto_completo = f"{nome} {descricao}".lower()
    
    categorias = {
        'cozinha': ['panela', 'frigideira', 'cozinha', 'cozinhar', 'mixer', 'liquidificador', 'microondas', 'geladeira'],
        'quarto': ['cama', 'travesseiro', 'lençol', 'quarto', 'colchão', 'edredom'],
        'sala': ['sofá', 'poltrona', 'mesa', 'televisão', 'tv', 'sala', 'centro'],
        'banheiro': ['toalha', 'banheiro', 'chuveiro', 'sabonete', 'shampoo'],
        'eletronicos': ['eletrônico', 'smartphone', 'tablet', 'notebook', 'computador', 'tv', 'som']
    }
    
    for categoria, palavras in categorias.items():
        if any(palavra in texto_completo for palavra in palavras):
            return categoria
    
    return 'casa'

def extrair_preco_numerico(preco_texto):
    """Converte texto de preço para número decimal"""
    try:
        # Remover caracteres não numéricos exceto vírgula e ponto
        numeros = re.sub(r'[^\d,.]', '', str(preco_texto))
        
        # Converter vírgula para ponto se for decimal brasileiro
        if ',' in numeros and '.' not in numeros:
            numeros = numeros.replace(',', '.')
        elif ',' in numeros and '.' in numeros:
            # Formato brasileiro: 1.234,56
            numeros = numeros.replace('.', '').replace(',', '.')
        
        return float(numeros) if numeros else 0.0
    except:
        return 0.0
