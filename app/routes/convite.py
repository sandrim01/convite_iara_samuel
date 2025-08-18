from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.models import db, Convidado, ConfiguracaoSite, Presente, EscolhaPresente
from datetime import datetime

convite = Blueprint('convite', __name__)

@convite.route('/<token>')
def convite_personalizado(token):
    """Convite personalizado para cada convidado"""
    convidado = Convidado.query.filter_by(token=token).first()
    if not convidado:
        abort(404)
    
    config = ConfiguracaoSite.query.first()
    presentes_disponiveis = Presente.query.filter_by(disponivel=True).all()
    presentes_escolhidos = EscolhaPresente.query.filter_by(convidado_id=convidado.id).all()
    
    return render_template('convite/convite_personalizado.html', 
                         convidado=convidado, 
                         config=config,
                         presentes_disponiveis=presentes_disponiveis,
                         presentes_escolhidos=presentes_escolhidos)

@convite.route('/<token>/confirmar', methods=['POST'])
def confirmar_presenca(token):
    """Confirmar presença do convidado"""
    convidado = Convidado.query.filter_by(token=token).first()
    if not convidado:
        abort(404)
    
    convidado.confirmou_presenca = True
    convidado.data_confirmacao = datetime.utcnow()
    convidado.acompanhantes = int(request.form.get('acompanhantes', 0))
    convidado.observacoes = request.form.get('observacoes')
    
    db.session.commit()
    
    flash('Presença confirmada com sucesso! Obrigado!', 'success')
    return redirect(url_for('convite.convite_personalizado', token=token))

@convite.route('/<token>/escolher-presente/<int:presente_id>', methods=['POST'])
def escolher_presente(token, presente_id):
    """Escolher um presente da lista"""
    convidado = Convidado.query.filter_by(token=token).first()
    if not convidado:
        abort(404)
    
    presente = Presente.query.get_or_404(presente_id)
    
    # Verificar se o presente ainda está disponível
    if not presente.disponivel:
        flash('Este presente já foi escolhido por outro convidado.', 'error')
        return redirect(url_for('convite.convite_personalizado', token=token))
    
    # Verificar se o convidado já escolheu este presente
    escolha_existente = EscolhaPresente.query.filter_by(
        convidado_id=convidado.id,
        presente_id=presente_id
    ).first()
    
    if escolha_existente:
        flash('Você já escolheu este presente!', 'info')
        return redirect(url_for('convite.convite_personalizado', token=token))
    
    # Criar nova escolha
    escolha = EscolhaPresente(
        convidado_id=convidado.id,
        presente_id=presente_id
    )
    
    db.session.add(escolha)
    
    # Marcar presente como indisponível se necessário
    # (pode ser configurado para permitir múltiplas escolhas do mesmo presente)
    presente.disponivel = False
    
    db.session.commit()
    
    flash(f'Presente "{presente.nome}" escolhido com sucesso!', 'success')
    return redirect(url_for('convite.convite_personalizado', token=token))

@convite.route('/<token>/remover-presente/<int:escolha_id>', methods=['POST'])
def remover_presente(token, escolha_id):
    """Remover um presente da escolha do convidado"""
    convidado = Convidado.query.filter_by(token=token).first()
    if not convidado:
        abort(404)
    
    escolha = EscolhaPresente.query.filter_by(
        id=escolha_id,
        convidado_id=convidado.id
    ).first_or_404()
    
    # Tornar o presente disponível novamente
    presente = escolha.presente
    presente.disponivel = True
    
    db.session.delete(escolha)
    db.session.commit()
    
    flash(f'Presente "{presente.nome}" removido da sua lista!', 'info')
    return redirect(url_for('convite.convite_personalizado', token=token))
