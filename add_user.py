from app import app, db, User

with app.app_context():
    new_user = User(username='admin', password='password123')
    db.session.add(new_user)
    db.session.commit()
    print("Test user added successfully.")
