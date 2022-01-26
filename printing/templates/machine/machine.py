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

    context = {"user": User}
    return render_template("/machine/machine_main.html", **context)
