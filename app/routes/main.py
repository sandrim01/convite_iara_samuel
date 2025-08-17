from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import ConfiguracaoSite, Presente, Convidado
from app import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Página inicial do convite"""
    config = ConfiguracaoSite.query.first()
    if not config:
        # Criar configuração padrão se não existir
        config = ConfiguracaoSite(
            nome_noiva='Iara',
            nome_noivo='Samuel',
            mensagem_principal='Com muito amor, convidamos você para celebrar conosco o nosso grande dia!'
        )
        db.session.add(config)
        db.session.commit()
    
    return render_template('index.html', config=config)

@main.route('/lista-presentes')
def lista_presentes():
    """Página da lista de presentes geral"""
    presentes = Presente.query.filter_by(disponivel=True).all()
    return render_template('lista_presentes.html', presentes=presentes)
