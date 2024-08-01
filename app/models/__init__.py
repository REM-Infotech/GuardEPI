from app.models.Funcionários import *
from app.models.users import *
from app.models.EPI import *


from app import db
from app import app
from app.misc import generate_pid

with app.app_context():
    
    db.create_all()
    
    usr = Users.query.filter_by(login = "root").first()
    
    if usr is None:
        
        usr = Users(
            
            login = "root",
            nome_usuario = "Root",
            email = "nicholas@robotz.dev",
            
            
        )
        root_pw = generate_pid(10)
        usr.senhacrip = root_pw
        db.session.add(usr)
        db.session.commit()
        print(f"* Root Pw: {root_pw}")

