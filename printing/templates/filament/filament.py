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
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

bp_filament = Blueprint("filament", __name__)


@bp_filament.route("/", methods=["GET", "POST"])
@login_required
def filament_main():
    fils = Filament.query.all()
    context = {'user': User, 'fils': fils}
    return render_template("/filament/filament_main.html", **context)


@bp_filament.route("/add", methods=["GET", "POST"])
@login_required
def filament_add():
    form = Filament_form()
    if form.validate_on_submit():
        fil = Filament()
        form.populate_obj(fil)
        db.session.add(fil)
        db.session.commit()
        return redirect(url_for("bp_filament.filament_main"))

    return render_template("/filament/filament_add.html", user=User, form=form)
