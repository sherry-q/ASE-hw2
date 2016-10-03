# reference tutorial: https://www.tutorialspoint.com/flask/flask_sqlalchemy.htm

from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shopping_list.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class shopping_list(db.Model):
   # class definition
   id = db.Column('item_id', db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   quantity = db.Column(db.String(50))

   def __init__(self, name, quantity):
      self.name = name
      self.quantity = quantity

@app.route('/')
def home():
   # display homepage
   return render_template('home.html', list = shopping_list.query.all() )

@app.route('/new', methods = ['GET', 'POST'])
def new():
   # add record to database
   if request.method == 'POST':
      if not request.form['name'] or not request.form['quantity']:
         flash('Please enter all the fields', 'error')
      else:
         # get item from input
         item = shopping_list(request.form['name'], request.form['quantity'])
         db.session.add(item)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('home'))
   return render_template('new.html')

@app.route('/remove', methods = ['GET', 'POST'])
def remove():
   # remove record from database
   if request.method == 'POST':
      if not request.form['name'] or not request.form['quantity']:
         flash('Please enter all the fields', 'error')
      else:
         # get item from input
         item = shopping_list(request.form['name'], request.form['quantity'])
         to_delete = shopping_list.query.filter_by(name=request.form['name']).first()
         db.session.delete(to_delete)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('home'))
   return render_template('new.html')

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)