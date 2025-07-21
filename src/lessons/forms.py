from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class LessonForm(FlaskForm):
    title = StringField('Tên bài học', validators=[DataRequired(message='Trường này là bắt buộc.')])
    description = TextAreaField('Mô tả')
    submit = SubmitField('Thêm bài học')
