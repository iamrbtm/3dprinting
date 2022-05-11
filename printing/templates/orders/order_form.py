from flask_wtf import FlaskForm
import email_validator, flask_login
from wtforms import (
    StringField,
    DateField,
    DecimalField,
    IntegerField,
    PasswordField,
    SelectField,
    SelectMultipleField,
    SubmitField,
    FloatField,
    FileField,
    HiddenField,
)
from wtforms.validators import InputRequired, Email, URL, NumberRange
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms_sqlalchemy.orm import model_form
from printing import db
from printing.models import *


class Order_Form(FlaskForm):
    list_machine = lambda: [(m.id, m.name) for m in Machine.query.all()]
    list_filament = lambda: [(f.id, f.dropdown_display()) for f in Filament.query.all()]
    list_customer = lambda: [
        (c.id, c.fullname())
        for c in Customer.query.filter(Customer.customer_status == 1).all()
    ]
    orderstatus = lambda: [
        (c.id, c.status)
        for c in Status.query.filter(Status.whatfor == "Orders / Projects").all()
    ]

    date_needed = DateField("Date Needed", [InputRequired()])
    project_name = StringField("Project Name", [InputRequired()])
    customerfk = SelectField("Customer", [], choices=list_customer)
    order_status = SelectField("Status", [], choices=orderstatus)
    machinefk = SelectField("Machine", [], choices=list_machine)
    filamentfk = SelectField("Filament", [], choices=list_filament)
    gcode = FileField("Gcode File", [InputRequired()])
    qty = IntegerField(
        "Quantity",
        [
            NumberRange(min=1, max=100, message="Must be a number from 1 to 100"),
            InputRequired(),
        ],
    )
    setuptime = StringField("Pre print setup time (in min)")
    taredowntime = StringField("Post print setup time (in min)")
    postprocessingtime = StringField("Time in Min for post processing")
