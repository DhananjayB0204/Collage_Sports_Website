from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, TextAreaField, DateField
from wtforms.validators import InputRequired, Length
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sport_database.db'
app.config['UPLOAD_FOLDER'] = 'static/images'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)  # Make sure the field name matches

class Sport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_filename = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50), nullable=False)

# Forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

class SportForm(FlaskForm):
    name = StringField('Sport Name', validators=[InputRequired(), Length(max=100)])
    date = StringField('Date', validators=[InputRequired()])
    image = FileField('Upload Image', validators=[InputRequired()])

class NoticeForm(FlaskForm):
    title = StringField('Notice Title', validators=[InputRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[InputRequired(), Length(max=200)])
    date = StringField('Date', validators=[InputRequired()])  # Date field

@app.route('/', methods=['GET', 'POST'])
def home():
    form = LoginForm()
    notices = Notice.query.all()
    return render_template('index.html', form=form, notices=notices)

@app.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            flash('Login successful!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Login failed. Please check your username and password.', 'danger')
            return redirect(url_for('home'))
    return render_template('index.html', form=form)

@app.route('/logout')
def logout():
    # Clear the session or any other logout logic
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))  # Redirect to the home (index) page

@app.route('/notices', methods=['GET', 'POST'])
def notices():
    form = NoticeForm()
    if form.validate_on_submit():
        new_notice = Notice(
            title=form.title.data,
            description=form.description.data,
            date=form.date.data
        )
        db.session.add(new_notice)
        db.session.commit()
        
        flash('Notice added successfully!', 'success')
        return redirect(url_for('notices'))

    notices = Notice.query.all()
    return render_template('notice.html', form=form, notices=notices)


@app.route('/delete_notice/<int:notice_id>', methods=['POST'])
def delete_notice(notice_id):
    notice = Notice.query.get_or_404(notice_id)
    db.session.delete(notice)
    db.session.commit()
    flash('Notice deleted successfully!', 'success')
    return redirect(url_for('notices'))

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/upload_banner', methods=['POST'])
def upload_banner():
    if 'banner_image' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('admin'))
    file = request.files['banner_image']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('admin'))
    if file:
        filename = secure_filename('B1.jpeg')  # Save as B1.jpeg
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Banner uploaded successfully!', 'success')
        return redirect(url_for('admin'))
    else:
        flash('Something went wrong. Try again.', 'danger')
        return redirect(url_for('admin'))

@app.route('/sports_sec', methods=['GET', 'POST'])
def sports_sec():
    form = SportForm()
    if form.validate_on_submit():
        file = form.image.data
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_sport = Sport(name=form.name.data, image_filename=filename, date=form.date.data)
        db.session.add(new_sport)
        db.session.commit()

        flash('Sport added successfully!', 'success')
        return redirect(url_for('sports_sec'))

    sports = Sport.query.all()
    return render_template('sports_sec.html', form=form, sports=sports)

@app.route('/delete_sport/<int:sport_id>', methods=['POST'])
def delete_sport(sport_id):
    sport = Sport.query.get_or_404(sport_id)
    db.session.delete(sport)
    db.session.commit()
    flash('Sport deleted successfully!', 'success')
    return redirect(url_for('sports_sec'))

if __name__ == '__main__':
    app.run(debug=True)
