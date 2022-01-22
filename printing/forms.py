from flask_wtf import FlaskForm
import email_validator, flask_login
from wtforms import (
    StringField,
    DateField,
    DecimalField,
    PasswordField,
    SelectField,
    SelectMultipleField,
    SubmitField,
    FloatField,
    HiddenField
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
    vendor = lambda:[(c.id, c.name) for c in Vendors.query.all()]
    types = lambda:[(c.id, c.type) for c in Type.query.all()]
    name = StringField("Name (Internal Use only)", [InputRequired()])
    color = StringField("Color", [InputRequired()])
    priceperroll = FloatField(
        "Cost of Roll", [NumberRange(min=0.01, max=9999, message="Enter numbers only")]
    )
    length_spool = SelectField("Spool Length", [], choices=[(1, "1.75mm"), (2, "3mm")])
    url = StringField("Purchase Website", [])
    purchasedate = DateField("Purchase Date")
    vendorfk = SelectField("Vendor",[],choices=vendor)
    typefk = SelectField("Type", [], choices=types)
    submit = SubmitField("Submit")


class Type_form(FlaskForm):
    bed_temps = [
        "5",
        "10",
        "15",
        "20",
        "25",
        "30",
        "35",
        "40",
        "45",
        "50",
        "55",
        "60",
        "65",
        "70",
        "75",
        "80",
        "85",
        "90",
        "95",
        "100",
        "105",
        "110",
        "115",
        "120",
        "125",
    ]
    ext_temps = [
        "150",
        "155",
        "160",
        "165",
        "170",
        "175",
        "180",
        "185",
        "190",
        "195",
        "200",
        "205",
        "210",
        "215",
        "220",
        "225",
        "230",
        "235",
        "240",
        "245",
        "250",
        "255",
        "260",
        "265",
        "270",
        "275",
        "280",
        "285",
        "290",
        "295",
        "300",
    ]
    type = StringField("Type of Filament", [InputRequired()])
    properties = StringField("Properties", [])
    useage = StringField("Uses", [])
    diameter = SelectMultipleField(
        u"Diameter", [], coerce=int, choices=[(1, "1.75mm"), (2, "3mm")], default=[1,2]
    )
    extruder_temp_from = SelectField(u"End Temp Start Range", choices=ext_temps)
    extruder_temp_to = SelectField(u"End Temp End Range", choices=ext_temps)
    bed_temp_from = SelectField(u"Bed Temp From Range", choices=bed_temps)
    bed_temp_to = SelectField(u"Bed Temp To Range", choices=bed_temps)
    bed_adhesion = StringField(u"Bed Adhesion")
    densitygcm3 = DecimalField(u"Density")
    m_in_1kg_3 = DecimalField(u"Meters in 1 KG (3mm diameter)")
    m_in_1kg_175 = DecimalField(u"Meters in 1 KG (3mm diameter)")
    submit = SubmitField(u"Submit")
