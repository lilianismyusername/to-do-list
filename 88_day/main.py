from flask import Flask,render_template,redirect,url_for,request,flash
from flask_bootstrap import Bootstrap
from wtforms import SubmitField,TextAreaField,DateField,validators,TimeField,StringField
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.secret_key = 'jsldkjflksjlkdjfkjls'
Bootstrap(app)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# -----------------------------------------------------------------------------------database
class database(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer,nullable=False,primary_key=True)
    date = db.Column(db.String,nullable=False)
    todo = db.Column(db.String,nullable=False)
    time = db.Column(db.String,nullable=False)
    date_n = db.Column(db.Integer,nullable=False)
    time_n = db.Column(db.Integer,nullable=False)
    font_color = db.Column(db.String)

class color_database(db.Model):
    __tablename__ = 'color'
    id = db.Column(db.Integer,primary_key = True)
    red = db.Column(db.String)
    black = db.Column(db.String)
    green = db.Column(db.String)

class todo_form(FlaskForm):
    date = DateField(label='Date',validators= [validators.DataRequired()])
    todo = TextAreaField(label='todo',validators=[validators.DataRequired()])
    time = TimeField(label='time',validators=[validators.DataRequired()])
    submit = SubmitField()

class color_form(FlaskForm):
    green = StringField(label='Green')
    red = StringField(label='Red')
    black = StringField(label='Black')
    submit = SubmitField()

db.create_all()
db.session.commit()

# item = color_database(red='',green='',black='')
# db.session.add(item)
# db.session.commit()
print(str(datetime.datetime.today().date()).replace('-',''))
print(str(datetime.datetime.today().time()).replace(':',''))
@app.route('/',methods=['POST','GET'])
def home():
    global green_list,red_list
    form = todo_form()

    all_forms = database.query.order_by(database.date_n,database.time_n).all()

    if request.method == 'POST':

        if (not(form.date.data) or not(form.todo.data) or not(form.time.data)) and not(request.form.get('delete')) and not(request.form.get('red')) and not(request.form.get('green'))  and not(request.form.get('black')) and not (request.args.get('key') == 'value'):
            flash('fill the field!')
            return redirect(url_for('home'))

        if request.form.get('delete'):
            del_item = database.query.get(int(request.form.get('delete')))
            db.session.delete(del_item)
            db.session.commit()
            return redirect(url_for('home'))

        if request.form.get('red'):

            red = int(request.form.get('red'))
            update = database.query.get(red)
            update.font_color = 'red'
            db.session.commit()

            return redirect(url_for('home'))

        if request.form.get('green'):
            green = int(request.form.get('green'))
            update = database.query.get(green)
            update.font_color = 'green'
            db.session.commit()

            return redirect(url_for('home'))

        if request.form.get('black'):
            black = int(request.form.get('black'))
            update = database.query.get(black)
            update.font_color = 'black'
            db.session.commit()

            return redirect(url_for('home'))

        date = str(form.date.data)
        todo = form.todo.data
        time = str(form.time.data)
        data = database(date=date,todo=todo,time=time,date_n=int(date.replace('-','')),time_n=int(time.replace(':','')),font_color='black')
        db.session.add(data)
        db.session.commit()
        all_forms = database.query.order_by(database.date_n,database.time_n).all()

    return render_template('index.html', form=form, todo_lists=all_forms,color_form=color_form(),black=color_database.query.get(1).black,green=color_database.query.get(1).green,red=color_database.query.get(1).red,today_date = int(str(datetime.datetime.today().date()).replace('-','')),today_time=float(str(datetime.datetime.today().time()).replace(':','')))

@app.route('/color_form',methods=['POST','GET'])
def color():

    color = color_form()
    if request.method == 'POST':
        color_ = color_database.query.get(1)
        if color.red.data:
            color_.red = color.red.data
        if color.black.data:
            color_.black = color.black.data
        if color.green.data:
            color_.green = color.green.data

        db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
