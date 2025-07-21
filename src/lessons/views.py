
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .models import Lesson
from .forms import LessonForm
from src import db

lessons_bp = Blueprint('lessons', __name__)

@lessons_bp.route('/lessons/add', methods=['GET', 'POST'], endpoint='add')
@login_required
def add():
    if getattr(current_user, 'role', None) != 'giangvien':
        flash('Bạn không có quyền truy cập chức năng này.', 'danger')
        return redirect(url_for('accounts.dashboard_lecturer'))
    form = LessonForm()
    if form.validate_on_submit():
        lesson = Lesson(
            title=form.title.data,
            description=form.description.data,
            created_by=current_user.id
        )
        db.session.add(lesson)
        db.session.commit()
        flash('Thêm bài học thành công!', 'success')
        return redirect(url_for('accounts.dashboard_lecturer'))
    return render_template('lessons/add_lesson.html', form=form)

@lessons_bp.route('/lessons', endpoint='index')
@login_required
def index():
    lessons = Lesson.query.order_by(Lesson.created_at.desc()).all()
    return render_template('lessons/lessons.html', lessons=lessons)


@lessons_bp.route('/lessons/<int:lesson_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    if getattr(current_user, 'role', None) != 'giangvien' or lesson.created_by != current_user.id:
        flash('Bạn không có quyền sửa bài học này.', 'danger')
        return redirect(url_for('lessons.index'))
    form = LessonForm(obj=lesson)
    if form.validate_on_submit():
        lesson.title = form.title.data
        lesson.description = form.description.data
        db.session.commit()
        flash('Cập nhật bài học thành công!', 'success')
        return redirect(url_for('lessons.index'))
    return render_template('lessons/edit_lesson.html', form=form, lesson=lesson)

@lessons_bp.route('/lessons/<int:lesson_id>/delete', methods=['POST'])
@login_required
def delete_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    if getattr(current_user, 'role', None) != 'giangvien' or lesson.created_by != current_user.id:
        flash('Bạn không có quyền xóa bài học này.', 'danger')
        return redirect(url_for('lessons.index'))
    db.session.delete(lesson)
    db.session.commit()
    flash('Đã xóa bài học.', 'success')
    return redirect(url_for('lessons.index'))
    form = LessonForm()
    if form.validate_on_submit():
        lesson = Lesson(
            title=form.title.data,
            description=form.description.data,
            created_by=current_user.id
        )
        db.session.add(lesson)
        db.session.commit()
        flash('Thêm bài học thành công!', 'success')
        return redirect(url_for('accounts.dashboard_lecturer'))
    return render_template('lessons/add_lesson.html', form=form)
