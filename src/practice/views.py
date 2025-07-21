import io
import sys
from flask import Blueprint, render_template, request
from flask_login import login_required

practice_bp = Blueprint('practice', __name__)

@practice_bp.route('/practice', methods=['GET', 'POST'])
@login_required
def practice():
    code = ''
    output = ''
    if request.method == 'POST':
        code = request.form['code']
        try:
            # Bắt output từ print()
            old_stdout = sys.stdout
            sys.stdout = mystdout = io.StringIO()

            exec(code, {})  # Chạy mã Python

            output = mystdout.getvalue()  # Lấy kết quả từ print()
            sys.stdout = old_stdout  # Khôi phục lại stdout
        except Exception as e:
            sys.stdout = old_stdout
            output = f"❌ Lỗi: {str(e)}"
    return render_template('practice/practice.html', code=code, output=output)
