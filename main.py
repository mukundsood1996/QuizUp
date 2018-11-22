from flask import Flask, request, render_template, url_for, flash, session
from werkzeug.utils import redirect
import database.db_access as db

app = Flask(__name__)
app.config['SECRET_KEY'] = '59d3ca27e6701d3fd06eb960ca5866a5'


@app.route("/", methods=["GET"])
@app.route("/home", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if('user_id' in session):
        return render_template("index.html")

    data = request.form.to_dict(flat=False)
    print("login data ",data)

    if(data):
        data['email'] = ''.join(data['email'])
        data['password'] = ''.join(data['password'])

        response = db.validate_users(**data)

        if(response is not "invalid"):
            session['user_id'] = response
            print("response ", response)
            return render_template("index.html")
        flash("invalid email or password")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    data = request.form.to_dict(flat=False)

    print("register data ",data)
    if(data):
        data['name'] = ''.join(data['name'])
        data['email'] = ''.join(data['email'])
        data['password'] = ''.join(data['password'])

        response = db.register_users(**data)
        if(response):
            return redirect(url_for('login'))
        flash("user Exists")
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