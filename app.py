from flask import Flask, render_template, redirect, url_for, flash
from forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'pythonsecret'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def home():
    return render_template("base.html")

@app.route("/auth", methods=['GET', 'POST'])
def auth():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for("profile"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.password == form.password.data:
            login_user(user)
    return render_template("auth.html", form = form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    return render_template('register.html', form=form)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/logout")
def logout():
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