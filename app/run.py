import os

from flask_bootstrap import Bootstrap5
from flask import Flask, request, redirect, url_for
from flask import render_template as original_render_template
from flask_login import LoginManager, current_user, login_user, login_required, logout_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm

from wtforms import EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from utils.util_var import subscription_plans, members_list, moods_list, occasions_list

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app._static_folder = os.path.abspath("app/static/")
app.secret_key = "Ke2c'01/sba!P23."

login_manager = LoginManager()
login_manager.init_app(app)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQL_STRING']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Users(db.Model, UserMixin):
    id = db.Column("id", db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(1000), nullable=False)
    __table_args__ = {'schema': 'magikard'}
    

    def __init__(self, fname, lname, email, password, code, verified):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class RegistrationForm(FlaskForm):
    fname = StringField('First Name', validators=None)
    lname = StringField('Last Name', validators=None)
    email = EmailField('Email address *', validators=[DataRequired()])
    password = PasswordField('Password *', validators=[DataRequired(), Length(min=8, max=20)])
    submit = SubmitField('Sign up')


class LogInForm(FlaskForm):
    email = EmailField('Email address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign in')


def render_template(*args, **kwargs):
    return original_render_template(*args, **kwargs, is_user=current_user.is_authenticated)

@login_manager.user_loader
def load_user(id):
   return Users.query.get(int(id))

@app.route('/')
def home():
    return render_template("index.html", subscription_plans=subscription_plans)

@app.route('/about')
def about():
    return render_template('about.html', members_list=members_list)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/forgetpassword')
def reset():
    return render_template('resetpassword.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('logout.html')

@app.route('/create')
def create():
    if current_user.is_authenticated:
        return render_template('createcard.html', moods_list=moods_list, occasions_list=occasions_list)
    else:
        return redirect(url_for("login"))

@app.route('/download')
@login_required
def download():
    return render_template('download.html')

@app.route('/login', methods=['POST', 'GET'])
def login(success=False):
    warning=False
    login_form = LogInForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data

        user = Users.query.filter_by(email=email).first()

        if user is not None and user.check_password(password):
            login_user(user)
            return render_template('index.html', subscription_plans=subscription_plans)
        else:
            warning=True
    return render_template('login.html', form=login_form, warning=warning, success=request.args.get('success'))

@app.route('/signup', methods=['POST', 'GET'])
def register():
    warning=False
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        fname = registration_form.fname.data
        lname = registration_form.lname.data
        email = registration_form.email.data
        password = registration_form.password.data

        user_count = Users.query.filter_by(email=email).count()

        if(user_count > 0):
            warning=True
        else:
            user = Users(fname, lname, email, password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login", success=True))
    return render_template('register.html', form=registration_form, warning=warning)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(401)
def not_authorized(e):
    return render_template('401.html'), 401

if __name__ == "__main__":
    db.create_all()

    if db.session.query(Users.email).filter_by(email='admin@admin.com').first() is None:
        admin_user = Users(None, None, "admin@admin.com", "admin")
        db.session.add(admin_user)
        db.session.commit()

    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)