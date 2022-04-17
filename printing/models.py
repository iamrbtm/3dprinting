from printing import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import datetime, os
from sqlalchemy.orm import backref, relationship
from sqlalchemy import ForeignKey


# Users
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    address = db.Column(db.String(150))
    city = db.Column(db.String(150))
    state = db.Column(db.String(2))
    zip = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(150), unique=True)
    dob = db.Column(db.Date)
    avatar_filename = db.Column(db.Text)
    avatar_url = db.Column(db.String(250))
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())


class apitoken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    token = db.Column(db.String(200))


class States(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(50))
    abr = db.Column(db.String(2))


class Vendors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    url = db.Column(db.String(250))
    address = db.Column(db.String(150))
    city = db.Column(db.String(150))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.String(20))
    userid = db.Column(db.Integer)
    update_time = db.Column(
        db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    # Relationships
    filament = db.relationship("Filament", backref="vendors", lazy=True)


class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100))
    properties = db.Column(db.JSON)
    useage = db.Column(db.JSON)
    diameter = db.Column(db.JSON)
    # filament info
    extruder_temp = db.Column(db.JSON)
    bed_temp = db.Column(db.JSON)
    bed_adhesion = db.Column(db.JSON)
    densitygcm3 = db.Column(db.Float)
    m_in_1kg_3 = db.Column(db.Float)
    m_in_1kg_175 = db.Column(db.Float)

    userid = db.Column(db.Integer)
    update_time = db.Column(
        db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    # Relationships
    filament_rel = db.relationship("Filament", backref="type", lazy=True)


class Filament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    color = db.Column(db.String(100))
    colorhex = db.Column(db.String(20))
    priceperroll = db.Column(db.Float)
    length_spool = db.Column(db.Integer)
    diameter = db.Column(db.Float)
    url = db.Column(db.String(200))
    purchasedate = db.Column(db.Date)
    picture = db.Column(db.String(100))
    userid = db.Column(db.Integer)
    update_time = db.Column(
        db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    #Forign Key
    vendorfk = db.Column(db.Integer, db.ForeignKey("vendors.id"))
    typefk = db.Column(db.Integer, db.ForeignKey("type.id"))
    fil_status = db.Column(db.Integer, db.ForeignKey("status.id"))
    # Relationships
    type_rel = db.relationship("Type", backref="filament", lazy=True)
    status_rel = db.relationship("Status", backref="filament", lazy=True)

    def dropdown_display(self):
        return self.name + " (" + self.type_rel.type + ")"


class Machine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    purchase_price = db.Column(db.Float)
    purchase_date = db.Column(db.Date)
    make = db.Column(db.String(50))
    model = db.Column(db.String(50))
    serial_number = db.Column(db.String(50), unique=True)
    picture = db.Column(db.String(100))
    mach_icon = db.Column(db.String(100))
    c_roi_per_min = db.Column(db.Float)
    userid = db.Column(db.Integer)
    update_time = db.Column(
        db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    # Forign Key
    machine_status = db.Column(db.Integer, db.ForeignKey("status.id"))
    # Relationships
    infourl_rel = db.relationship("Info_url", backref="machine", lazy=True)
    status_rel = db.relationship("Status", backref="machine", lazy=True)


class Info_url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(300))
    description = db.Column(db.Text)
    catagory = db.Column(db.String(75))
    userid = db.Column(db.Integer)
    update_time = db.Column(
        db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    # forign Keys
    machinefk = db.Column(db.Integer, db.ForeignKey("machine.id"))


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(150))
    lname = db.Column(db.String(150))
    company = db.Column(db.String(150))
    address = db.Column(db.String(150))
    address2 = db.Column(db.String(150))
    city = db.Column(db.String(150))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(150), unique=True)
    markuppercent = db.Column(db.Float)
    userid = db.Column(db.Integer)
    #Forign Keys
    customer_status = db.Column(db.Integer, db.ForeignKey("status.id"))
    # Relationship
    orders_rel = db.relationship("Orders", backref="customer", lazy=True)
    status_rel = db.relationship("Status", backref="customer", lazy=True)

    
    def fullname(self):
        return self.fname + " " + self.lname
    
    def csz(self):
        return self.city +", "+self.state +" "+self.zipcode


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_needed = db.Column(db.Date)
    project_name = db.Column(db.String(100), unique=True)
    qty = db.Column(db.Integer)
    weight_in_g = db.Column(db.String(10))
    time_to_print = db.Column(db.String(50))
    setuptime = db.Column(db.Integer)
    taredowntime = db.Column(db.Integer)
    time = db.Column(db.Integer)
    c_labor = db.Column(db.Float)
    c_machine = db.Column(db.Float)
    c_materials = db.Column(db.Float)
    c_markup = db.Column(db.Float)
    shipping = db.Column(db.Float)
    userid = db.Column(db.Integer)
    update_time = db.Column(
        db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    # Forign Key
    customerfk = db.Column(db.Integer, db.ForeignKey("customer.id"))
    order_status = db.Column(db.Integer, db.ForeignKey("status.id"))
    machinefk = db.Column(db.Integer, db.ForeignKey("machine.id"))
    filamentfk = db.Column(db.Integer, db.ForeignKey("filament.id"))
    # Relationship
    machine_rel = db.relationship("Machine", backref="orders", lazy=True)
    filament_rel = db.relationship("Filament", backref="orders", lazy=True)
    status_rel = db.relationship("Status", backref="orders", lazy=True)
    customer_rel = db.relationship("Customer", backref="orders", lazy=True)

    def subtotal(self):
        return self.c_labor+self.c_machine+self.c_markup+self.c_materials
    
    def total(self):
        return "${:,.2f}".format((self.subtotal() + self.shipping)* self.qty) 
        
        
class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50))
    description = db.Column(db.Text)
    color = db.Column(db.String(10))
    whatfor = db.Column(db.String(50))
    userid = db.Column(db.Integer)
    update_time = db.Column(
        db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())


class Colors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(10))
    hexcolor = db.Column(db.String(10))

class Setup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pricePerHour = db.Column(db.Float)
    userid = db.Column(db.Integer)
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())



# class <name>(db.Model):
#     id = db.Column(db.Integer, primary_key=True)

#     userid = db.Column(db.Integer)
#     update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
#     date_created = db.Column(db.DateTime(timezone=True), default=func.now())
