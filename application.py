from crypt import methods
from os import abort
from flask import Flask, render_template,redirect,request,flash,url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__,template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite'
app.secret_key = 'dev'

db = SQLAlchemy(app)



class students(db.Model):
   id = db.Column('student_id', db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   city = db.Column(db.String(50))  
   addr = db.Column(db.String(200))
   pin = db.Column(db.String(10))

   def __init__(self, name, city, addr,pin):
        self.name = name
        self.city = city
        self.addr = addr
        self.pin = pin
        db.create_all()

@app.route("/show_all")
def show_all():
    return render_template('show_all.html',students = students.query.all())



@app.route("/play")
def play():
    return render_template('play.html')



@app.route("/layout")
def layout():
    return render_template('layout.html')


#@app.route('/<int:id>/edit',methods=['GET','POST'])
#def update(id):
#   student = students.query.filter_by(id=id).first()
 #  if request.method == "POST":
 #              student = students(request.form['name'], request.form['city'],request.form['addr'], request.form['pin'])

  # return render_template('update.html', student = student)



@app.route('/<int:id>/delete',methods=['GET','POST'])
def delete(id):
   student = students.query.filter_by(id=id).first()
   if request.method == 'POST':
      if student:
         db.session.delete(student)
         db.session.commit()
         return redirect('/show_all')
      abort(404)
   return render_template('delete.html')




@app.route('/add', methods = ['GET', 'POST'])
def add():
   if request.method == 'POST':
      if not request.form['name'] or not request.form['city'] or not request.form['addr']:
         flash('Please enter all the fields', 'error')
      else:
         student = students(request.form['name'], request.form['city'],request.form['addr'], request.form['pin'])
         
         db.session.add(student)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('add.html')



@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['name'] or not request.form['city'] or not request.form['addr']:
         flash('Please enter all the fields', 'error')
      else:
         student = students(request.form['name'], request.form['city'],request.form['addr'], request.form['pin'])
         
         db.session.add(student)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('add.html')




if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)


