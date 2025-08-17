from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

class Admin(UserMixin, db.Model):
    """Modelo para administradores (o casal)"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Convidado(db.Model):
    """Modelo para convidados"""
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    token = db.Column(db.String(100), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    confirmou_presenca = db.Column(db.Boolean, default=False)
    data_confirmacao = db.Column(db.DateTime, nullable=True)
    acompanhantes = db.Column(db.Integer, default=0)
    observacoes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com presentes escolhidos
    presentes_escolhidos = db.relationship('EscolhaPresente', backref='convidado', lazy=True)

class Presente(db.Model):
    """Modelo para lista de presentes"""
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    categoria = db.Column(db.String(50), nullable=True)
    preco_sugerido = db.Column(db.Float, nullable=True)
    link_loja = db.Column(db.String(500), nullable=True)
    imagem_url = db.Column(db.String(500), nullable=True)
    disponivel = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com escolhas
    escolhas = db.relationship('EscolhaPresente', backref='presente', lazy=True)

class EscolhaPresente(db.Model):
    """Modelo para registrar escolhas de presentes pelos convidados"""
    id = db.Column(db.Integer, primary_key=True)
    convidado_id = db.Column(db.Integer, db.ForeignKey('convidado.id'), nullable=False)
    presente_id = db.Column(db.Integer, db.ForeignKey('presente.id'), nullable=False)
    data_escolha = db.Column(db.DateTime, default=datetime.utcnow)
    entregue = db.Column(db.Boolean, default=False)
    data_entrega = db.Column(db.DateTime, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)

class ConfiguracaoSite(db.Model):
    """Modelo para configurações gerais do site"""
    id = db.Column(db.Integer, primary_key=True)
    nome_noiva = db.Column(db.String(100), default='Iara')
    nome_noivo = db.Column(db.String(100), default='Samuel')
    data_casamento = db.Column(db.Date, nullable=True)
    local_cerimonia = db.Column(db.String(200), nullable=True)
    endereco_cerimonia = db.Column(db.Text, nullable=True)
    horario_cerimonia = db.Column(db.Time, nullable=True)
    local_festa = db.Column(db.String(200), nullable=True)
    endereco_festa = db.Column(db.Text, nullable=True)
    horario_festa = db.Column(db.Time, nullable=True)
    mensagem_principal = db.Column(db.Text, nullable=True)
    cor_tema = db.Column(db.String(7), default='#ff69b4')  # Rosa como padrão
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
