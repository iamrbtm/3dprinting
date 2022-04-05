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
from printing.utilities import *
from printing.forms import *
import datetime

bp_status = Blueprint("status", __name__)

@bp_status.route('/', methods=['GET', 'POST'])
def status_home():
    form = Status_Form()

    if form.validate_on_submit():
        stat = Status()
        form.populate_obj(stat)
        stat.userid = current_user.id
        db.session.add(stat)
        db.session.commit()
        return redirect(url_for("status.status_home"))

    stats = Status.query.all()
    
    context = {'user': User, 'form':form, 'stats':stats}
    return render_template("/status/status_home.html", **context)


@bp_status.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def status_edit(id):
    db_stats = db.session.query(Status).filter_by(id = id).first()
    form = Status_Form(obj=db_stats)
    if form.validate_on_submit():
        db_stats.status = form.status.data
        db_stats.description = form.description.data
        db_stats.color = form.color.data
        db_stats.whatfor = form.whatfor.data
        db_stats.userid = current_user.id
        db.session.commit()
        return redirect(url_for('status.status_home'))
    
    form.process(obj=db_stats)
   
    context = {'user': User, 'form':form, 'status':db_stats}
    return render_template("/status/status_edit.html", **context)