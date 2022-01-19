from flask_wtf import FlaskForm
import email_validator
from wtforms import (
    StringField,
    DateField,
    PasswordField,
    SelectField,
    SubmitField,
    FloatField,
)
from wtforms.validators import InputRequired, Email, URL, NumberRange
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms_sqlalchemy.orm import model_form
from printing import db
from printing.models import *


class User_form(FlaskForm):
    fname = StringField("First Name", [InputRequired()])
    lname = StringField("Last Name", [InputRequired()])
    address = StringField("Address", [])
    city = StringField("City", [])
    state = SelectField("State")
    zipcode = StringField("Zip Code", [])
    phone = StringField("Phone", [])
    email = StringField("Email Address", [InputRequired(), Email()])
    dob = DateField("Date of Birth", [InputRequired()])
    username = StringField("User Name", [InputRequired()])
    password = PasswordField("Password", [InputRequired()])
    submit = SubmitField("Update Profile")

    def __init__(self):
        super(User_form, self).__init__()
        self.state.choices = [(c.abr, c.state) for c in States.query.all()]


class Filament_form(FlaskForm):
    name = StringField("Name (Internal Use only)", [InputRequired()])
    color = StringField("Color", [InputRequired()])
    priceperroll = FloatField(
        "Cost of Roll", [NumberRange(min=0.01, max=9999, message="Enter numbers only")]
    )
    length_spool = FloatField(
        "Spool Length", [NumberRange(min=0.01, max=9999, message="Enter numbers only")]
    )
    url = StringField("Purchase Website", [URL()])
    purchasedate = DateField("Purchase Date")
    vendorfk = SelectField("Vendor")
    typefk = SelectField("Type", [InputRequired()])

    def __init__(self):
        super(Filament_form, self).__init__()
        self.typefk.choices = [
            (
                c.id,
                c.type
                + " (Bed: "
                + c.bed_temp[0]
                + u"\N{DEGREE SIGN}C"
                + "-"
                + c.bed_temp[1]
                + u"\N{DEGREE SIGN}C"
                + " - HotEnd: "
                + c.extruder_temp[0]
                + u"\N{DEGREE SIGN}C"
                + "-"
                + c.extruder_temp[1]
                + u"\N{DEGREE SIGN}C"
                + ")",
            )
            for c in Type.query.all()
        ]
        self.vendorfk.choices = [(c.id, c.name) for c in Vendors.query.all()]
        self.color.choices = [c.color for c in db.session.query(Filament.color).all()]
