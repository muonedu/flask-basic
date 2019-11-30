from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
db = SQLAlchemy(app)

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "restaurant.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# -------------------------- Database Area ----------------------

class Restaurant(db.Model):
	id = db.Column(db.Integer, unique=True, primary_key=True)
	name = db.Column(db.String(150))
	price = db.Column(db.Integer)
	amount = db.Column(db.Integer)
	marks = db.Column(db.Text)

	def __repr__(self):
		return self.name
# ------------------------------------------------------------------

# routing for homepage ('/')
@app.route('/')
def index():
	items = Restaurant.query.all()
	return render_template('index.html', data=items)

@app.route('/showItem')
def show():
	items = [ 'Rendang', 'Ayam', 'Ikan', 'Teh es']
	return render_template('index.html', items=items)

@app.route('/addItem', methods=["GET", "POST"])
def additem():
	if request.method == 'POST':
		nameItem = request.form['name']
		price = int(request.form['price'])
		amount = request.form['amount']
		marks = request.form['marks']

		#check database
		item = Restaurant.query.filter_by(name=nameItem).first()
		if not item:
			new_item = Restaurant(name=nameItem, price=price, amount=amount, marks=marks)
			db.session.add(new_item)
			db.session.commit()
			result = {
				'message': 'Data has been added'
			}
			return redirect('/')
		if item:
			return render_template('index.html')
	else:
		return render_template('index.html')

@app.route('/showPrice')
def showPrice():
	items = {
		'item_a' : {
			'name': 'Rendang',
			'price': 20000
			},
		'item_b' : {
			'name': 'Ayam',
			'price': 15000
			},
		'item_c' : {
			'name': 'Ikan',
			'price': 10000
			},
		'item_d' : {
			'name': 'Teh es',
			'price': 5000}
	}
	return items

if __name__ == '__main__':
	app.run(debug=True, port=1000)
