from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

from cloudipsp import Api, Checkout

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/margaritasmyslava/PycharmProjects/CFG/pythonProject/pythonProject/onlinemarket/shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy()
db.init_app(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'Written Data: {self.title}'
@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all() # take items from table and show it in return
    return render_template('index.html', data=items)



@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/buy/<int:id>')
def item_buy(id):
    item = Item.query.get(id)

    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "EUR",
        "amount": str(item.price) + '00'
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)

@app.route('/create', methods=['POST', 'GET'])  # track data  from post
def create():
    if request.method != 'POST':
        return render_template('create.html')

    title = request.form['title']
    price = request.form['price']
    text = request.form['text']

    item = Item(title=title, price=price, text=text)

    db.session.add(item)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':  # if we start all our projest starting with main.py
    app.run(debug=True)  # show our error on webpage(after deploy-> True)
