from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = "supersecret"


class LoginForm(FlaskForm):
    login = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit_to = SubmitField()
title = f'Homelab Hub'

@app.route('/')
def index():
    return render_template('index.html', title=title)

@app.route('/news')
def news():
    return render_template('news.html', title=title)

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
    
    return render_template('profile.html', title=title, login=login, password=password, form=form)