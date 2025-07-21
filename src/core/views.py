from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

core_bp = Blueprint("core", __name__)


@core_bp.route("/")
@login_required
def home():
    if hasattr(current_user, 'role') and current_user.role == 'giaovien':
        return redirect(url_for('accounts.dashboard_lecturer'))
    return render_template("core/index.html")