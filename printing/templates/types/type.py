from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    after_this_request,
    flash,
)
from flask_login import login_required, current_user
import flask_login
from sqlalchemy.orm import session
from printing.models import *
from printing.templates.base.base_process import *
from printing import db, photos
from printing.forms import *
from printing.utilities import *
import datetime

bp_type = Blueprint("type", __name__)


@bp_type.route("/", methods=["GET", "POST"])
@login_required
def filament_main():
    form = Type_form()
    
    types = Type.query.all()
    context = {'user': User, 'fils': fils, 'types':types, 'form':form}
    return render_template("/filament/filament_main.html", **context)

# @bp_filament.route("/edit/<int:id>", methods=["GET", "POST"])
# @login_required
# def filament_edit(id):
#     form = Filament_form()
#     db_fil = db.session.query(Filament).filter_by(id = id).first()
#     if form.validate_on_submit():
#         fil = Filament()
#         form.populate_obj(fil)
#         fil.userid = current_user.id
#         db.session.add(fil)
#         db.session.commit()
#         return redirect(url_for("filament.filament_main"))
    
#     form.name.data = db_fil.name
#     form.color.data = db_fil.color
#     form.priceperroll.data = db_fil.priceperroll
#     form.length_spool.data = db_fil.length_spool
#     form.url.data = db_fil.url
#     form.purchasedate.data = db_fil.purchasedate
#     form.vendorfk.data = db_fil.vendorfk #TODO figure out how to get the selected / stored value to populate in the select.
#     form.typefk.data = form.typefk.choices[db_fil.typefk-1] #TODO figure out how to get the selected / stored value to populate in the select.

#     types = Type.query.all()
#     context = {'user': User, 'types':types, 'form':form}
#     return render_template("/filament/filament_edit.html", **context)
