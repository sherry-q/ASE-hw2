"""Shopping list app"""
# reference tutorial: https://www.tutorialspoint.com/flask/flask_sqlalchemy.htm

from flask import Flask, request, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shopping_list.sqlite3'
app.config['SECRET_KEY'] = "9cHmmg00EE"

db = SQLAlchemy(app)

class shopping_list(db.Model):
	"""Shopping list class"""
	# class definition
	id = db.Column('item_id', db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	quantity = db.Column(db.String(50))

	def __init__(self, name, quantity):
		self.name = name
		self.quantity = quantity

@app.route('/')
def home():
	"""Display homepage"""
	return render_template('home.html', list=shopping_list.query.all())

@app.route('/new', methods=['GET', 'POST'])
def new():
	"""Add record to database"""
	if request.method == 'POST':
		if not request.form['name'] or not request.form['quantity']:
			return render_template('form_incomplete.html')
		else:
			# get item from input and add
			item = shopping_list(request.form['name'], request.form['quantity'])
			db.session.add(item)
			db.session.commit()
			return redirect(url_for('home'))
	return render_template('new.html')

@app.route('/remove', methods=['GET', 'POST'])
def remove():
	"""Remove record from database"""
	if request.method == 'POST':
		# check if item exists
		if db.session.query(shopping_list.id).filter \
		(shopping_list.name == request.form['name']).count() < 1:
			return render_template('not_found.html')
		else:
			# get item from input and remove
			to_delete = shopping_list.query.filter_by(name=request.form['name']).first()
			db.session.delete(to_delete)
			db.session.commit()
			return redirect(url_for('home'))
	return render_template('new.html')

if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)
