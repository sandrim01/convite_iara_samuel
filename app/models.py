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
    foto_casal = db.Column(db.String(500), nullable=True)  # URL (compatibilidade)
    foto_casal_blob = db.Column(db.LargeBinary, nullable=True)  # Imagem armazenada
    foto_casal_filename = db.Column(db.String(255), nullable=True)  # Nome original
    foto_casal_mimetype = db.Column(db.String(100), nullable=True)  # Tipo MIME
    
    # Campos do casal
    descricao_noiva = db.Column(db.Text, nullable=True)
    aniversario_noiva = db.Column(db.String(50), nullable=True)
    paixoes_noiva = db.Column(db.String(200), nullable=True)
    frase_noiva = db.Column(db.String(200), nullable=True)
    foto_noiva = db.Column(db.String(500), nullable=True)  # URL (compatibilidade)
    foto_noiva_blob = db.Column(db.LargeBinary, nullable=True)  # Imagem armazenada
    foto_noiva_filename = db.Column(db.String(255), nullable=True)  # Nome original
    foto_noiva_mimetype = db.Column(db.String(100), nullable=True)  # Tipo MIME
    
    descricao_noivo = db.Column(db.Text, nullable=True)
    aniversario_noivo = db.Column(db.String(50), nullable=True)
    paixoes_noivo = db.Column(db.String(200), nullable=True)
    frase_noivo = db.Column(db.String(200), nullable=True)
    foto_noivo = db.Column(db.String(500), nullable=True)  # URL (compatibilidade)
    foto_noivo_blob = db.Column(db.LargeBinary, nullable=True)  # Imagem armazenada
    foto_noivo_filename = db.Column(db.String(255), nullable=True)  # Nome original
    foto_noivo_mimetype = db.Column(db.String(100), nullable=True)  # Tipo MIME
    
    # História de amor - opcionais
    mostrar_historia = db.Column(db.Boolean, default=True)
    primeiro_encontro_ano = db.Column(db.String(10), nullable=True)
    primeiro_encontro_texto = db.Column(db.Text, nullable=True)
    namoro_ano = db.Column(db.String(10), nullable=True)
    namoro_texto = db.Column(db.Text, nullable=True)
    pedido_ano = db.Column(db.String(10), nullable=True)
    pedido_texto = db.Column(db.Text, nullable=True)
    grande_dia_ano = db.Column(db.String(10), nullable=True)
    grande_dia_texto = db.Column(db.Text, nullable=True)
    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_foto_url(self, tipo):
        """Retorna a URL da foto: prioriza link externo (Instagram/URL), senão upload."""
        if tipo == 'casal':
            if self.foto_casal:
                return self.foto_casal
            elif self.foto_casal_blob:
                return f'/image/casal/{self.id}'
        elif tipo == 'noiva':
            if self.foto_noiva:
                return self.foto_noiva
            elif self.foto_noiva_blob:
                return f'/image/noiva/{self.id}'
        elif tipo == 'noivo':
            if self.foto_noivo:
                return self.foto_noivo
            elif self.foto_noivo_blob:
                return f'/image/noivo/{self.id}'
        return None
    
    def has_foto(self, tipo):
        """Verifica se tem foto (upload ou link)"""
        if tipo == 'casal':
            return self.foto_casal_blob is not None or bool(self.foto_casal)
        elif tipo == 'noiva':
            return self.foto_noiva_blob is not None or bool(self.foto_noiva)
        elif tipo == 'noivo':
            return self.foto_noivo_blob is not None or bool(self.foto_noivo)
        return False

class Convidado(db.Model):
    """Modelo para convidados"""
    __tablename__ = 'convidado'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    token = db.Column(db.String(100), unique=True, nullable=False)
    confirmacao = db.Column(db.Boolean, default=False)  # True = confirmou, False = não confirmou
    data_confirmacao = db.Column(db.DateTime, nullable=True)
    numero_acompanhantes = db.Column(db.Integer, default=0)
    eventos_participara = db.Column(db.String(200), nullable=True)  # cerimonia,festa
    restricoes_alimentares = db.Column(db.Text, nullable=True)
    mensagem = db.Column(db.Text, nullable=True)
    liberado_recepcao = db.Column(db.Boolean, default=False)  # Liberado para ver convite de recepção
    convite_enviado_whatsapp = db.Column(db.Boolean, default=False)  # Controla se convite foi enviado via WhatsApp
    data_envio_whatsapp = db.Column(db.DateTime, nullable=True)  # Data do último envio
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Compatibilidade com código antigo
    @property
    def confirmou_presenca(self):
        return self.confirmacao
    
    @confirmou_presenca.setter
    def confirmou_presenca(self, value):
        self.confirmacao = value
    
    @property
    def acompanhantes(self):
        return self.numero_acompanhantes
    
    @acompanhantes.setter
    def acompanhantes(self, value):
        self.numero_acompanhantes = value
    
    @property
    def observacoes(self):
        return self.mensagem
    
    @observacoes.setter
    def observacoes(self, value):
        self.mensagem = value
    
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
    nome_presenteador = db.Column(db.String(100), nullable=True)
    email_presenteador = db.Column(db.String(120), nullable=True)
    telefone_presenteador = db.Column(db.String(20), nullable=True)
    mensagem = db.Column(db.Text, nullable=True)
    data_escolha = db.Column(db.DateTime, default=datetime.utcnow)
    entregue = db.Column(db.Boolean, default=False)
    data_entrega = db.Column(db.DateTime, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<EscolhaPresente {self.convidado_id}-{self.presente_id}>'
