from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

class Admin(UserMixin, db.Model):
    """Modelo para administradores do sistema"""
    __tablename__ = 'admin'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        """Define a senha criptografada"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica se a senha está correta"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Admin {self.username}>'

class ConfiguracaoSite(db.Model):
    """Configurações gerais do site de casamento"""
    __tablename__ = 'configuracao_site'
    
    id = db.Column(db.Integer, primary_key=True)
    nome_noiva = db.Column(db.String(100), default='Iara')
    nome_noivo = db.Column(db.String(100), default='Samuel')
    data_casamento = db.Column(db.Date, nullable=True)
    local_cerimonia = db.Column(db.Text, nullable=True)
    endereco_cerimonia = db.Column(db.Text, nullable=True)
    horario_cerimonia = db.Column(db.Time, nullable=True)
    local_festa = db.Column(db.Text, nullable=True)
    endereco_festa = db.Column(db.Text, nullable=True)
    horario_festa = db.Column(db.Time, nullable=True)
    mensagem_principal = db.Column(db.Text, default='Criamos esse site para compartilhar com vocês os detalhes da organização do nosso casamento. ♥')
    cor_tema = db.Column(db.String(7), default='#d4a574')  # Rosa/dourado
    foto_casal = db.Column(db.String(500), nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Convidado(db.Model):
    """Modelo para convidados"""
    __tablename__ = 'convidado'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    token = db.Column(db.String(100), unique=True, nullable=False)
    confirmou_presenca = db.Column(db.Boolean, default=False)
    data_confirmacao = db.Column(db.DateTime, nullable=True)
    acompanhantes = db.Column(db.Integer, default=0)
    observacoes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com presentes escolhidos
    presentes_escolhidos = db.relationship('EscolhaPresente', backref='convidado', lazy=True)
    
    def __repr__(self):
        return f'<Convidado {self.nome}>'

class Presente(db.Model):
    """Modelo para presentes da lista"""
    __tablename__ = 'presente'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    categoria = db.Column(db.String(50), nullable=True)
    preco_sugerido = db.Column(db.Numeric(10, 2), nullable=True)
    link_loja = db.Column(db.String(500), nullable=True)
    imagem_url = db.Column(db.String(500), nullable=True)
    disponivel = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com escolhas
    escolhas = db.relationship('EscolhaPresente', backref='presente', lazy=True)
    
    @property
    def foi_escolhido(self):
        """Verifica se o presente já foi escolhido"""
        return len(self.escolhas) > 0
    
    def __repr__(self):
        return f'<Presente {self.nome}>'

class EscolhaPresente(db.Model):
    """Modelo para relacionar convidados com presentes escolhidos"""
    __tablename__ = 'escolha_presente'
    
    id = db.Column(db.Integer, primary_key=True)
    convidado_id = db.Column(db.Integer, db.ForeignKey('convidado.id'), nullable=False)
    presente_id = db.Column(db.Integer, db.ForeignKey('presente.id'), nullable=False)
    data_escolha = db.Column(db.DateTime, default=datetime.utcnow)
    entregue = db.Column(db.Boolean, default=False)
    data_entrega = db.Column(db.DateTime, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<EscolhaPresente {self.convidado_id}-{self.presente_id}>'
