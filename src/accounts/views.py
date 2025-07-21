from src.utils import get_b64encoded_qr_image
from .forms import LoginForm, RegisterForm, ChangePasswordForm
from src.accounts.models import User
from src import db, bcrypt
from flask_login import current_user, login_required, login_user, logout_user
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask import session


accounts_bp = Blueprint("accounts", __name__)

HOME_URL = "core.home"
SETUP_2FA_URL = "accounts.setup_two_factor_auth"
VERIFY_2FA_URL = "accounts.verify_two_factor_auth"


@accounts_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("Bạn đã đăng ký rồi.", "info")
        return redirect(url_for(HOME_URL))

    form = RegisterForm(request.form)

    if form.validate_on_submit():
        try:
            # ✅ Mã hóa mật khẩu trước khi lưu
            hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")

            user = User(
                username=form.username.data,
                password=hashed_pw,
                role=form.role.data
            )

            db.session.add(user)
            db.session.commit()


            flash("Tài khoản đã được tạo.", "success")
            return redirect(url_for("accounts.login"))
        except Exception as e:
            db.session.rollback()
            flash("Đăng ký không thành công. Vui lòng thử lại.", "danger")
            print("Registration Error:", e)

    return render_template("accounts/register.html", form=form)


@accounts_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(HOME_URL))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Đăng nhập thành công!", "success")
            if user.role == "giangvien":
                return redirect(url_for("accounts.dashboard_lecturer"))
            elif user.role == "admin":
                return redirect(url_for("admin.users"))
            else:
                return redirect(url_for(HOME_URL))
        else:
            flash("Tên đăng nhập hoặc mật khẩu không đúng", "danger")
    return render_template("accounts/login.html", form=form)

@accounts_bp.route("/lecturer/dashboard")
@login_required
def dashboard_lecturer():
    if current_user.role != "giangvien":
        flash("Bạn không có quyền truy cập.", "danger")
        return redirect(url_for(HOME_URL))
    return render_template("accounts/dashboard_lecturer.html")


@accounts_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Bạn đã đăng xuất.", "success")
    return redirect(url_for("accounts.login"))



@accounts_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        # Kiểm tra mật khẩu hiện tại đúng
        if not bcrypt.check_password_hash(current_user.password, form.current_password.data):
            flash("Mật khẩu hiện tại không đúng", "danger")
        else:
            # Đổi mật khẩu mới
            hashed_pw = bcrypt.generate_password_hash(form.new_password.data).decode("utf-8")
            current_user.password = hashed_pw
            db.session.commit()
            flash("Đổi mật khẩu thành công", "success")

    return render_template("accounts/profile.html", form=form)
