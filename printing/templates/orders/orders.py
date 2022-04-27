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
from sqlalchemy import or_, and_
from sqlalchemy.orm import session
from printing.models import *
from printing.templates.base.base_process import *
from printing import db, photos
from printing.templates.orders.order_form import *
from printing.templates.orders.process_orders import *
from printing.utilities import *
import datetime

bp_order = Blueprint("order", __name__)

@bp_order.route("/", methods=["GET", "POST"])
def order_home():
    orders = Orders.query.filter(and_(Orders.order_status !=8, Orders.order_status!=18)).all()
    context = {"user": User, "orders":orders}
    return render_template("/orders/order_home.html", **context)


@bp_order.route("/add", methods=["GET", "POST"])
def order_add():
    form = Order_Form()

    if form.validate_on_submit():
        neworder = Orders()
        if form.gcode.data:
            parsetime, parseweight, filused, time = get_raw_data(
                form.filamentfk.data, form.gcode.data
            )
            neworder.time_to_print = parsetime
            neworder.weight_in_g = parseweight
            neworder.time = time
        form.populate_obj(neworder)
        neworder.userid = current_user.id
        db.session.add(neworder)
        db.session.commit()
        cost = calculate_cost(neworder, filused)
        neworder.c_materials = cost["materials"]
        neworder.c_markup = cost["markup"]
        neworder.c_labor = cost["labor"]
        neworder.c_machine = cost["machine"]
        neworder.shipping = 0
        db.session.commit()
        return redirect(url_for("order.order_home"))

    context = {"user": User, "form": form}
    return render_template("/orders/order_add.html", **context)


@bp_order.route("/details/<id>", methods=["GET", "POST"])
def order_details(id):
    order_data = db.session.query(Orders).filter(Orders.id == id).first()
    form = Order_Form(obj=order_data)
    subtotal = order_data.c_materials + order_data.c_machine + order_data.c_labor + order_data.c_markup
    total = order_data.shipping + subtotal
    totaltime = calc_total_time((order_data.setuptime + order_data.taredowntime), order_data.time)

    context = {"user": User, "order": order_data, "subtotal": subtotal, "total":total, "totaltime":totaltime, "form":form}
    return render_template("/orders/order_details.html", **context)

@bp_order.route('/update/<id>/<orderstatus>')
def update(id, orderstatus):
    order_data = db.session.query(Orders).filter(Orders.id == id).first()
    order_data.order_status = orderstatus
    db.session.commit()
    return redirect(url_for('order.order_details', id=id))
    
@bp_order.route('/check/<id>')
def check(id):
    order = Orders.query.filter(Orders.id == id).first()
    return render_template("/emails/status_printing.html", order=order)
    
    
# [x]: DETAILS page
# [x]: incorperate uploading a file with putting parsed info in the system
# [x]: link to order when clicked on cuatomer page
# [x]]: put orders on the main menu
# [ ]: fix to where the order details come up when clicking on the customer page.
# [x]: figure out why the connection keeps getting reset when adding an order... does it have naything to do with the triggers I set up?
# [w]: Email the customer when the order status changes
