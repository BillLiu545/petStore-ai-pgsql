from db import db;

class Customer(db.Model):
    __tablename__ = 'customers'
    
    user_name = db.Column(db.String(50), nullable=False, primary_key=True)
    f_name = db.Column(db.String(50), nullable=False)
    l_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
    def __repr__(self):
        return f'<customers {self.user_name} {self.f_name} {self.l_name} {self.email} {self.password}>'