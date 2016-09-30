from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class shopping_list(db.Model):
   id = db.Column('item', db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   quantity = db.Column(db.String(100))

   def __init__(self, name, quantity):
      self.name = name
      self.quantity = quantity

@app.route('/')
def show_all():
   return render_template('show_all.html', shopping_list = shopping_list.query.all() )

@app.route('/form', methods = ['GET', 'POST'])
def form():
   if request.method == 'POST':
      if not request.form['name'] or not request.form['quantity']:
         flash('Please enter all the fields', 'error')
      else:
         item = shopping_list(request.form['name'], request.form['quantity'])  
         if request.form['add']:
            db.session.add(item)
            db.session.commit()
            flash('Record was successfully added')
         else:
            db.session.delete(item)
            db.session.commit()
            flash('Record was successfully removed')
         return redirect(url_for('show_all'))
   return render_template('form.html')
"""
@app.route('/remove', methods = ['GET', 'POST'])
def remove():
   if request.method == 'POST':
      if not request.form['name'] or not request.form['city'] or not request.form['addr'] or not request.form['pin']:
         flash('Please enter all the fields', 'error')
      else:
         student = students(request.form['name'], request.form['city'], request.form['addr'], request.form['pin'])
         db.session.delete(student)
         db.session.commit()
         flash('Record was successfully removed')
         return redirect(url_for('show_all'))
   return render_template('new.html')
"""

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)