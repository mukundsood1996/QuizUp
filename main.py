from flask import Flask, request, render_template, url_for
from werkzeug.utils import redirect

app = Flask(__name__)


@app.route("/", methods=["GET"])
@app.route("/home", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    data = request.form.to_dict(flat=False)
    if(data):
        render_template("index.html")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    data = request.form.to_dict(flat=False)
    if(data):
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route("/quizzes", methods=["GET"])
def quizzes():
    return render_template("quizzes.html")


@app.route("/about_us", methods=["GET"])
def about_us():
    return render_template("about.html")


@app.route("/contact_us", methods=["GET"])
def contact_us():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
