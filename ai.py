import base64
import datetime
from sqlalchemy.dialects.postgresql import JSONB
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from openai import OpenAI
import psycopg2
from psycopg2.extras import RealDictCursor
from PIL import Image
import io
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
    cart=db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<customers {self.user_name} {self.f_name} {self.l_name} {self.email} {self.password} {self.cart}'
    
class Purchase(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    cust_name = db.Column(db.String(50), nullable=False)
    cart_items = db.Column(JSONB, nullable=False)
    card_num  = db.Column(db.String(16), nullable=False)
    buy_date = db.Column(db.DateTime, nullable=False)
    buy_time = db.Column(db.Time, nullable=False)
    num_items = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Numeric(10,2), nullable=False, default=0)
    def __repr__(self):
        return f'<purchase {self.id} {self.cust_name} {self.cart_items} {self.card_num} {self.buy_date} {self.buy_time} {self.num_items} {self.total_price}>'
    
with app.app_context():
    db.create_all()
    
def findName(user_name):
    conn = psycopg2.connect(
        host="aipc",
        database="ai_database",
        user="postgres",
        password="pgadminpass",
        port = 5432
    )
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT f_name, l_name, user_name FROM customer WHERE user_name = %s", (user_name,))
    result = cursor.fetchone()
    return jsonify({"name": result["f_name"] + " " + result["l_name"] + " (" + result["user_name"] + ")"})
    
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
        name= findName(data["user_name"])
        return name
    
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
        name= findName(data["user_name"])
        return name
def resize(img_bytes, size=(800,800)):
    img = Image.open(io.BytesIO(img_bytes))
    img.thumbnail(size)
    output = io.BytesIO()
    img.save(output, format='JPEG')
    return output.getvalue()

@app.route("/analyze", methods=["POST"])
def analyze():
    endpoint = "http://aipc:8787/v1/"
    client = OpenAI(api_key="api_key", base_url=endpoint)
    image = request.files['image']
    img_bytes = resize(image.read())
    encoded_img = base64.b64encode(img_bytes).decode('utf-8')
    response = client.chat.completions.create(
        model="Qwen/Qwen2.5-VL-7B-Instruct-AWQ",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Analyze this image of this pet I'm looking to adopt, and tell if it is in stock, and if so, provide its name, price and description in the following format: 'Name: <name>, Price: <price>, Description: <description>'. If it is not in stock, please say so. Since I am not using real-time data, randomly generate a number to tell if it is in stock, along with the price."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_img}"
                        }
                    }
                ]
            }
        ]
    )
    app.logger.info("Returning request...")
    return jsonify({"img_details": response.choices[0].message.content})
@app.route("/purchase", methods=["POST"])
def purchase(): 
    data = request.get_json(True)
    name = data["name"]
    cart_items = data["productList"]
    card_num = data["cardNum"]
    num_items = data["num_products"]
    now = datetime.datetime.now()
    rand_int = now.strftime("%Y%m%d%H%M%S")
    total_price = float(data.get("total_price",0))
    
    new_purchase = Purchase(
        id = rand_int,
        cust_name = name,
        cart_items = cart_items,
        card_num = card_num,
        buy_date = now.date(),
        buy_time = now.time(),
        num_items = num_items,
        total_price=total_price,
    )
    db.session.add(new_purchase)
    db.session.commit()
    return jsonify({"message": "Purchase successful", "purchase_id": new_purchase.id})
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0" , port=30000)
    
