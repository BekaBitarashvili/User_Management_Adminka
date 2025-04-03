from flask import Flask, render_template, redirect, url_for, flash, session
from forms import LoginForm, RegistrationForm
from extensions import db
from flask_login import UserMixin, current_user, login_user, login_required, logout_user
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'pythonsecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(20), unique=True, nullable=False)
    lastName = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"User('{self.firstName}', '{self.lastName}', '{self.email}')"

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/auth", methods=['GET', 'POST'])
def auth():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
              login_user(user)
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
        flash("You have been registered", "success")
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/profile")
@login_required
def profile():
    form = RegistrationForm()
    return render_template("profile.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
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