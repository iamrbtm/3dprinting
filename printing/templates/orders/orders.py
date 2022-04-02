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
    form = Order_Form()
    
    if form.validate_on_submit():
        print('Customer: '+form.customerfk.data)
        print('Machine: '+form.machinefk.data)
        print('Filament: '+form.filamentfk.data)
    
    context = {'user': User, 'form':form}
    return render_template("/orders/order_home.html", **context)