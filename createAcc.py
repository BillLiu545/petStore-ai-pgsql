from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pgadminpass@aipc:5432/ai_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Customer(db.Model):
    user_name=db.Column(db.String(50),nullable=False, primary_key=True)
    f_name=db.Column(db.String(50),nullable=False)
    l_name=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(120),nullable=False)
    password=db.Column(db.String(200),nullable=False)
    
    def __repr__(self):
        return f'<customers {self.user_name} {self.f_name} {self.l_name} {self.email} {self.password}'
    
    
with app.app_context():
    db.create_all()
    
@app.route("/create", methods=["POST"])
def create():
    data = request.get_json(True)
    new_acc = Customer (
        user_name = data["user_name"],
        f_name = data["f_name"],
        l_name = data["l_name"],
        email = data["email"],
        password = data["password"]
    )
    exists = Customer.query.filter_by(
        user_name = data["user_name"],
        password = data["password"]
    ).first()
    if exists:
        return jsonify({"message": "Account with this username and/or password already exists"})
    else:
        db.session.add(new_acc)
        db.session.commit()
        return jsonify({"message": 'Sign In Successful'})
    
@app.route("/sign", methods=["POST"])
def sign():
    data = request.get_json(True)
    exists = Customer.query.filter_by(
        user_name = data["user_name"],
       password = data["password"]
    ).first()
    if not exists:
        return jsonify({"message": "No account associated with this username and/or password"})
    else:
        return jsonify({"message": 'Sign In Successful'})
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0" , port=30000)