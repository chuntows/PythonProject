from src import create_app, db
from src.accounts.models import User  # điều chỉnh nếu đường dẫn khác

app = create_app()

with app.app_context():
    db.session.query(User).delete()
    db.session.commit()
    print("✅ Đã xoá toàn bộ người dùng.")
