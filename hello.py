from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + basedir + "/database.db"


db = SQLAlchemy()
db.init_app(app)


class Productes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    unitats = db.Column(db.Integer)
    photo = db.Column(db.String(255))  
    price = db.Column(db.Float)
    category_id = db.Column(db.Integer)
    seller_id = db.Column(db.Integer)
    created = db.Column(db.String(10))  
    updated = db.Column(db.String(10))  



@app.route('products/list')
def mostrar_list():
    return render_template('list.html', Productes=Productes)

@app.route('/')
def init():
    return 'Hello, World!'

@app.route('/hello/')
def hello():
    return render_template('hello.html')

if __name__ == '__main__':
    app.run()

