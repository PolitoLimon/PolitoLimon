from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + basedir + "/base_de_datos.db"


db = SQLAlchemy()
db.init_app(app)


class Productes(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    photo = db.Column(db.String)
    price = db.Column(db.Integer)
    # category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    # seller_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created = db.Column(db.DateTime, nullable=False, server_default= db.func.now())
    updated = db.Column(db.DateTime, nullable=False, server_default= db.func.now(), onupdate= db.func.now())


@app.route('/')
def init():
    return redirect(url_for('list'))

@app.route('/product')
def list():
    products = db.session.execute(
        db.select(Productes).order_by(Productes.id.asc())
    ).scalars()
    return render_template('/products/list.html', products = products)

@app.route('/product/<int:product_id>',methods = ['POST', 'GET'])
def item(product_id):
    # recupero l'item per la pk
    product = db.session.get(Productes, product_id)
    
    if request.method == 'GET':
        return render_template('item_update.html', product = Productes)
    else: # POST
        nom = request.form['nom']
        unitats = int(request.form['unitats']) # es text, el passo a enter

        # actualitzo els valors de l'item
        product.nom = nom
        product.unitats = unitats

        # notifico que item ha canviat i amb el commit és guarda a la BBDD
        db.session.add(item)
        db.session.commit()

        # https://en.wikipedia.org/wiki/Post/Redirect/Get
        return redirect(url_for('item', product_id = product_id))





if __name__ == '__main__':
    app.run()

