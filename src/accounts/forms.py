from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length, InputRequired

from src.accounts.models import User


class RegisterForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        "Repeat password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    # ✅ Thêm lựa chọn role
    role = SelectField('Vai trò', choices=[
        ('sinhvien', 'Sinh viên'),
        ('giangvien', 'Giảng viên')
    ], validators=[DataRequired()])

    def validate(self, extra_validators=None):
        initial_validation = super(RegisterForm, self).validate(extra_validators)
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        if self.password.data != self.confirm.data:
            self.password.errors.append("Passwords must match")
            return False
        return True


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Ghi nhớ đăng nhập")


    
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Mật khẩu hiện tại", validators=[DataRequired()])
    new_password = PasswordField("Mật khẩu mới", validators=[DataRequired()])
    confirm_password = PasswordField("Xác nhận mật khẩu", validators=[
        DataRequired(),
        EqualTo('new_password', message="Mật khẩu không khớp")
    ])
