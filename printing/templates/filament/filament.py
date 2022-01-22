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

bp_filament = Blueprint("filament", __name__)


@bp_filament.route("/", methods=["GET", "POST"])
@login_required
def filament_main():
    form = Filament_form()
    if form.validate_on_submit():
        fil = Filament()
        form.populate_obj(fil)
        fil.userid = current_user.id
        fil.colorhex = convert_color_to_hex(form.color.data)
        if form.url.data != '':
            fil.url = shorten_url(form.url.data)
        db.session.add(fil)
        db.session.commit()
        return redirect(url_for("filament.filament_main"))
    
    fils = Filament.query.all()
    types = Type.query.all()
    context = {'user': User, 'fils': fils, 'types':types, 'form':form}
    return render_template("/filament/filament_main.html", **context)

@bp_filament.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def filament_edit(id):
    db_fil = db.session.query(Filament).filter_by(id = id).first()
    form = Filament_form(obj=db_fil)
    if form.validate_on_submit():
        form.populate_obj(db_fil)
        db_fil.userid = current_user.id
        db.session.add(db_fil)
        db.session.commit()
        return redirect(url_for("filament.filament_main"))
    
    form.process(obj=db_fil)
   
    types = Type.query.all()
    context = {'user': User, 'types':types, 'form':form, 'filament':db_fil}
    return render_template("/filament/filament_edit.html", **context)

@bp_filament.route("/delete/<int:id>", methods=["GET", "POST"])
@login_required
def filament_delete(id):
    db.session.query(Filament).filter(Filament.id == id).delete()
    db.session.commit()
    return redirect(url_for('filament.filament_main'))