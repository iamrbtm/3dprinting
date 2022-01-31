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
from printing.forms import *
from printing.utilities import *
import datetime

bp_machine = Blueprint("machine", __name__)


@bp_machine.route("/", methods=["GET", "POST"])
@login_required
def machine_main():
    form = Machine_form()
    if form.validate_on_submit():
        newmachine = Machine()
        form.populate_obj(newmachine)
        newmachine.userid = current_user.id
        db.session.add(newmachine)
        db.session.commit()
        return redirect(url_for("machine.machine_main"))

    machines = db.session.query(Machine).all()
    context = {"user": User,
               "machines":machines,
               'form':form}
    return render_template("/machine/machine_main.html", **context)


@bp_machine.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def machine_edit(id):
    
    db_mac = db.session.query(Machine).filter_by(id = id).first()
    db_urs = db.session.query(Machine.infourl_rel).all()
    form = Machine_form(obj=db_mac)
    if form.validate_on_submit():
        form.populate_obj(db_mac)
        db_mac.userid = current_user.id
        db.session.add(db_mac)
        db.session.commit()
        return redirect(form.referer.data)
    
    form.process(obj=db_mac)
    form.referer.data = request.referrer
   
    context = {'user': User, 'form':form, 'machine':db_mac, 'db_urs':db_urs}
    return render_template("/machine/machine_edit.html", **context)


@bp_machine.route("/delete/<int:id>", methods=["GET", "POST"])
@login_required
def machine_delete(id):
    db.session.query(Machine).filter(Machine.id == id).delete()
    db.session.commit()
    return redirect(url_for('machine.machine_main'))
