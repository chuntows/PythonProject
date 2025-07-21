# WebPy - Đồ án Python Web

## Giới thiệu

WebPy là một dự án web được xây dựng bằng Python sử dụng Flask framework, hướng tới việc quản lý tài khoản, bài học, tiến độ học tập và tích hợp AI hỗ trợ giải thích kiến thức.

## Công nghệ sử dụng

- **Python 3**
- **Flask**: Framework web nhẹ, dễ mở rộng
- **Flask-Migrate/Alembic**: Quản lý migration database
- **SQLite**: Cơ sở dữ liệu mặc định
- **HTML/CSS**: Giao diện người dùng
- **Google Gemini API**: Tích hợp AI giải thích kiến thức

## Hướng dẫn cài đặt và chạy dự án

1. **Cài đặt thư viện: **
   pip install -r requirements.txt
2. **Khởi tạo database: **
   python manage.py db upgrade
3. **Chạy ứng dụng: **
   python manage.py run
4. **Truy cập: **
   - Mở trình duyệt và vào địa chỉ: http://127.0.0.1:5000

## Đóng góp

Mọi đóng góp, báo lỗi hoặc ý tưởng mới đều được hoan nghênh qua GitHub Issues hoặc Pull Request.

---

**Tác giả:** chuntows
