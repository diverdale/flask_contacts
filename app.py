import os
from flask import Flask, render_template, url_for, redirect, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, validators
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['BOOTSTRAP_USE_MINIFIED'] = True

db = SQLAlchemy(app)
Bootstrap(app)
Migrate(app, db)


@app.route("/")
def index():

    return render_template('index.html', current_app=current_app)


@app.route("/add", methods=['GET', 'POST'])
def add():

    form = ContactForm(request.form)

    if request.method == 'POST' and form.validate():
        new_contact = Contacts(first_name=form.first_name.data,
                               last_name=form.last_name.data,
                               street_address=form.street_address.data,
                               city=form.city.data,
                               state=form.state.data,
                               phone=form.phone.data)

        db.session.add(new_contact)
        db.session.commit()
        return redirect(url_for('list'))
    return render_template('add.html', form=form)


@app.route("/list")
def list():

    contacts = Contacts.query.all()

    return render_template('list.html', contacts=contacts)


@app.route("/details/<int:contact_id>")
def details(contact_id):
    contact = Contacts.query.filter_by(id=contact_id).first()

    return render_template('details.html', contact=contact)


class Contacts(db.Model):

    __tablename__ = 'contact'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    street_address = db.Column(db.String(100))
    city = db.Column(db.String(30))
    state = db.Column(db.String(30))
    phone = db.Column(db.String(15))

    def __init__(self, first_name, last_name, street_address, city, state, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.street_address = street_address
        self.city = city
        self.state = state
        self.phone = phone


class ContactForm(FlaskForm):
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])
    street_address = StringField('Street Address:', validators=[DataRequired()])
    city = StringField('City:', validators=[DataRequired()])
    state = StringField('State:', validators=[DataRequired()])
    phone = TelField('Phone Number:', validators=[DataRequired()])
    submit = SubmitField('Submit')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
