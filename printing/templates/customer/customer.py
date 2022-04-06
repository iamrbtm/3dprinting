from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    after_this_request,
    flash,
)
from sqlalchemy.sql.expression import func
from flask_login import login_required, current_user
import flask_login
from sqlalchemy.orm import session
from sqlalchemy import or_, and_
from printing.models import *
from printing.templates.base.base_process import *
from printing import db, photos
from printing.forms import *
from printing.utilities import *
import datetime, os

bp_customer = Blueprint("customer", __name__)


@bp_customer.route("/", methods=["GET", "POST"])
@login_required
def customer_main():
    form = customer_form()
    if form.validate_on_submit():
        cust = Customer()
        form.populate_obj(cust)
        cust.userid = current_user.id
        cust.phone = format_tel(form.phone.data)
        db.session.add(cust)
        db.session.commit()
        return redirect(url_for("customer.customer_main"))

    customers = Customer.query.all()
    context = {"user": User, "customers": customers, "form": form}
    return render_template("/customer/customer_main.html", **context)


@bp_customer.route("/detail/<int:id>", methods=["GET", "POST"])
@login_required
def customer_detail(id):

    db_cust = db.session.query(Customer).filter_by(id=id).first()
    form = customer_form(obj=db_cust)
    if form.validate_on_submit():
        db_cust.fname = form.fname.data
        db_cust.lname = form.lname.data
        db_cust.address = form.address.data
        db_cust.address2 = form.address2.data
        db_cust.city = form.city.data
        db_cust.state = form.state.data
        db_cust.zipcode = form.zipcode.data
        db_cust.phone = format_tel(form.phone.data)
        db_cust.email = form.email.data
        db_cust.userid = current_user.id
        db_cust.customer_status = form.customer_status.data
        db.session.commit()
        return redirect(url_for("customer.customer_main"))

    form.process(obj=db_cust)

    currentorders = (
        Orders.query.filter(Orders.customerfk == id)
        .filter(and_(Orders.order_status != 8, Orders.order_status != 18))
        .count()
    )
    pastorders = (
        Orders.query.filter(Orders.customerfk == id)
        .filter(or_(Orders.order_status == 8, Orders.order_status == 18))
        .count()
    )

    context = {
        "user": User,
        "form": form,
        "customer": db_cust,
        "currentorders": currentorders,
        "pastorders": pastorders,
    }
    return render_template("/customer/customer_detail.html", **context)


@bp_customer.route("/delete/<int:id>", methods=["GET", "POST"])
@login_required
def customer_delete(id):
    db.session.query(Customer).filter(Customer.id == id).delete()
    db.session.commit()
    return redirect(url_for("customer.customer_main"))
