from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = "supersecret"

db = SQLAlchemy(app)

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    e_mail = db.Column(db.String(100), nullable=False, unique=True)
    date_of_adding = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.login


class LoginForm(FlaskForm):
    login = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit_to = SubmitField()
    

class RegisterForm(FlaskForm):
    login_reg = StringField(validators=[DataRequired()])
    password_reg = PasswordField(validators=[DataRequired()])
    email_reg = EmailField(validators=[DataRequired()])
    submit_to_reg = SubmitField()


title = f'Homelab Hub'

@app.route('/')
def index():
    return render_template('index.html', title=title)

@app.route('/news')
def news():
    user_list = Users.query.order_by(Users.date_of_adding)
    return render_template('news.html', title=title, user_list=user_list)

@app.route('/about')
def about():
    return render_template('about.html', title=title)

@app.route('/projects')
def projects():
    return render_template('projects.html', title=title)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    login = None
    password = None
    form = LoginForm()
    
    if form.validate_on_submit():
        login = form.login.data
        password = form.password.data
        form.login.data = ''
        form.password.data = ''
        flash(f"Welcome back {login}!")
    
    return render_template('profile.html', title=title, login=login, password=password, form=form)

@app.route('/profile/register', methods=['GET', 'POST'])
def register():
    login_reg = None
    password_reg = None
    email_reg = None
    form = RegisterForm()
    
    if form.validate_on_submit():
        _user = Users.query.filter_by(e_mail=form.email_reg.data).first()
        if _user == None:
            _user = Users(login=form.login_reg.data, e_mail=form.email_reg.data, password=form.password_reg.data)
            db.session.add(_user)
            db.session.commit()
        login_reg = form.login_reg.data
        form.login_reg.data = ''
        form.password_reg.data = ''
        form.email_reg.data = ''
    
    return render_template('register.html', title=title, login_reg=login_reg, password_reg=password_reg, email_reg=email_reg, form=form)