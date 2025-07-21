
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from src.accounts.models import User
from src import db

admin_bp = Blueprint('admin', __name__)

# Xóa người dùng
@admin_bp.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'admin':
        flash('Không thể xóa tài khoản admin.', 'danger')
        return redirect(url_for('admin.users'))
    db.session.delete(user)
    db.session.commit()
    flash('Đã xóa người dùng.', 'success')
    return redirect(url_for('admin.users'))

# Chỉ cho admin truy cập
@admin_bp.before_request
def require_admin():
    if not current_user.is_authenticated or current_user.role != 'admin':
        flash('Bạn không có quyền truy cập trang quản trị.', 'danger')
        return redirect(url_for('core.home'))

# Danh sách người dùng
@admin_bp.route('/admin/users')
@login_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

# Chỉnh sửa thông tin người dùng
@admin_bp.route('/admin/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.username = request.form['username']
        db.session.commit()
        flash('Đã cập nhật thông tin người dùng.', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/edit_user.html', user=user)

# Phân quyền người dùng
@admin_bp.route('/admin/user/<int:user_id>/role', methods=['POST'])
@login_required
def change_role(user_id):
    user = User.query.get_or_404(user_id)
    new_role = request.form['role']
    if new_role in ['sinhvien', 'giangvien', 'admin']:
        user.role = new_role
        db.session.commit()
        flash('Đã thay đổi quyền người dùng.', 'success')
    else:
        flash('Vai trò không hợp lệ.', 'danger')
    return redirect(url_for('admin.users'))
