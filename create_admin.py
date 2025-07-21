from src import db, bcrypt, create_app
from src.accounts.models import User

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        if not User.query.filter_by(username='admin@gmail.com').first():
            u = User(username='admin@gmail.com', password=bcrypt.generate_password_hash('admin').decode('utf-8'), role='admin')
            db.session.add(u)
            db.session.commit()
            print('Admin user created!')
        else:
            print('Admin user already exists.')
