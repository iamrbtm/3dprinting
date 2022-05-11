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
from printing import db, photos, gcodefile, uploads
from printing.templates.orders.order_form import *
from printing.templates.orders.process_orders import *
from printing.utilities import *
import datetime

bp_order = Blueprint("order", __name__)


@bp_order.route("/", methods=["GET", "POST"])
def order_home():
    orders = Orders.query.filter(
        and_(Orders.order_status != 8, Orders.order_status != 18)
    ).all()
    context = {"user": User, "orders": orders}
    return render_template("/orders/order_home.html", **context)


@bp_order.route("/add", methods=["GET", "POST"])
def order_add():
    form = Order_Form()

    if form.validate_on_submit():
        ulfile = uploads.save(form.gcode.data)
        order = Ordering(form.filamentfk.data, form.setuptime.data, form.taredowntime.data, form.postprocessingtime.data, form.customerfk.data, form.machinefk.data, form.order_status.data, form.date_needed.data, form.project_name.data, form.qty.data, ulfile)
        order.add_to_db()
        return redirect(url_for("order.order_home"))

    context = {"user": User, "form": form}
    return render_template("/orders/order_add.html", **context)


@bp_order.route("/details/<id>", methods=["GET", "POST"])
def order_details(id):
    data = Orders.query.get_or_404(id)
    form = Order_Form(obj=data)
    order = Ordering(data.filamentfk,data.setuptime,
                     data.taredowntime, data.postprocessingtime,
                     data.customerfk, data.machinefk, data.order_status,
                     data.date_needed, data.project_name, data.qty, 
                     data.gcodefilename)
    order.send_to_db()
    context = {
        "user": User,
        "order": data,
        "subtotal": order.subtotal,
        "total": order.total,
        "totaltime": order.calculate_print_time(),
        "form": form,
    }
    return render_template("/orders/order_details.html", **context)


@bp_order.route("/update/<id>/<orderstatus>")
def update(id, orderstatus):
    data = db.session.query(Orders).filter(Orders.id == id).first()
    data.order_status = orderstatus
    db.session.commit()
    return redirect(url_for("order.order_details", id=id))


@bp_order.route("/check/<id>")
def check(id):
    order = Orders.query.filter(Orders.id == id).first()
    return render_template("/emails/status_printing.html", order=order)


@bp_order.route("/idk/<filid>/<fillength>/<s>/<t>/<p>/<cust>")
def idk(filid, fillength, cust, s=5, t=5, p=0):
    from printing.templates.orders.process_orders_class import Ordering

    order = Ordering(filid, fillength, s, t, p, cust)
    smt = f"<h1>Materials: {str(order.c_materials)}<br/>"
    smt = smt + f"Markup: {str(order.cost_markup())}<br/>"
    smt = smt + f"Labor: {str(order.cost_labor())}<br/>"
    smt = smt + f"</h1>"
    return smt


# [x]: DETAILS page
# [x]: incorperate uploading a file with putting parsed info in the system
# [x]: link to order when clicked on cuatomer page
# [x]]: put orders on the main menu
# [ ]: fix to where the order details come up when clicking on the customer page.
# [x]: figure out why the connection keeps getting reset when adding an order... does it have naything to do with the triggers I set up?
# [w]: Email the customer when the order status changes
