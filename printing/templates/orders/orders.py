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
from printing.models import *
from printing.templates.base.base_process import *
from printing import db, photos
from printing.templates.orders.order_form import *
from printing.utilities import *
import datetime

bp_order = Blueprint("order", __name__)

@bp_order.route('/', methods=['GET', 'POST'])
def order_home():
    from printing.templates.orders.process_orders import get_raw_data
    parsetime, parseweight = get_raw_data()
    form = Order_Form()
    
    if form.validate_on_submit():
        neworder = Orders()
        form.populate_obj(neworder)
        neworder.userid = current_user.id
        db.session.add(neworder)
        db.session.commit()
        return redirect(url_for("order.order_home"))
    
    context = {'user': User, 'form':form}
    return render_template("/orders/order_home.html", **context)