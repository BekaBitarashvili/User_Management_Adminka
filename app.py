from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/auth")
def auth():
    return render_template("auth.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)