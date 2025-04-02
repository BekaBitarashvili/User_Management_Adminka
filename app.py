from flask import Flask, render_template, redirect, url_for, flash, session
from forms import LoginForm, RegistrationForm
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from extensions import db

app = Flask(__name__)

app.config['SECRET_KEY'] = 'pythonsecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db.init_app(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(20), unique=True, nullable=False)
    lastName = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"User('{self.firstName}', '{self.lastName}', '{self.email}')"

USER_EMAIL = "test@gmail.com"
USER_PASS = "testtest"

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/auth", methods=['GET', 'POST'])
def auth():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == USER_EMAIL and form.password.data == USER_PASS:
            session["email"] = form.email.data
            flash("You are now logged in", "success")
            return redirect(url_for('home'))
        else:
            flash("Your Email or password is incorrect", "danger")
    return render_template("auth.html", form = form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(firstName=form.firstName.data, lastName=form.lastName.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
    return render_template('register.html', form=form)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/logout")
def logout():
    session.pop("email", None)
    flash('You have been successfully logged out','info')
    return render_template("base.html")


@app.errorhandler(403)
def error_403(e):
    return render_template("/errors/403.html"), 403

@app.errorhandler(404)
def error_404(e):
    return render_template("/errors/404.html"), 404

@app.errorhandler(500)
def error_500(e):
    return render_template("/errors/500.html"), 500

if __name__ == "__main__":
    app.run(debug=True)