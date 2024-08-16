from datetime import datetime
import bcrypt
from app import db
from app.misc import *
import pytz
salt = bcrypt.gensalt()


from flask_login import UserMixin
from flask import request
from app import login_manager

@login_manager.user_loader
def load_user(user_id):
    
    link = request.referrer
    if link is None:
        link = request.url
    
    return Users.query.get(int(user_id))
class Users(db.Model, UserMixin):
    
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(length=30), nullable=False, unique=True)
    nome_usuario = db.Column(db.String(length=64), nullable=False, unique=True)
    grupos = db.Column(db.String(length=1024), nullable=False)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password = db.Column(db.String(length=60), nullable=False)
    login_time = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Etc/GMT+4')))
    verification_code = db.Column(db.String(length=45),unique=True)
    login_id = db.Column(db.String(length=7), nullable=False, default = generate_pid())
    
    @property
    def senhacrip(self):
        return self.senhacrip
    
    @senhacrip.setter
    def senhacrip(self, senha_texto):
        self.password = bcrypt.hashpw(senha_texto.encode(), salt).decode("utf-8")

    def converte_senha(self, senha_texto_claro) -> bool:
        return bcrypt.checkpw(senha_texto_claro.encode("utf-8"), self.password.encode("utf-8"))

        
class Groups(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name_group = db.Column(db.String(length=30), nullable=False, unique=True)
    desc = db.Column(db.Text)
    members = db.Column(db.Text)
    perms = db.Column(db.Text)

class EndPoints(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(length=30), nullable=False, unique=True)
    displayName = db.Column(db.Text)


    