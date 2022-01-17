from flask_wtf import FlaskForm
import email_validator
from wtforms import StringField, DateField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email
from wtforms_sqlalchemy.fields import QuerySelectField
from printing import db
from printing.models import *

class User_form(FlaskForm):
    fname = StringField('First Name',[DataRequired()])
    lname = StringField('Last Name',[DataRequired()])
    address = StringField('Address',[])
    city = StringField('City',[])
    state = SelectField('State')
    zipcode = StringField('Zip Code', [])
    phone = StringField('Phone', [])
    email = StringField('Email Address', [DataRequired(), Email()])
    dob = DateField('Date of Birth', [DataRequired()])
    username = StringField('User Name', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Update Profile')
    
    def __init__(self):
        super(User_form, self).__init__()
        self.state.choices = [(c.abr, c.state) for c in States.query.all()]
    