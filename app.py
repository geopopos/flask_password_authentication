from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

class NameForm(FlaskForm):
    name = StringField("What is your name?")
    submit = SubmitField("Submit")

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        user = User(name=name)
        db.session.add(user)
        db.session.commit()
    users = User.query.all()
    return render_template('index.html', users=users, form=form)

if __name__ == '__main__':
    app.run(debug=True)