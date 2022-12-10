from flask import Flask, request, render_template, url_for, flash, session, jsonify
from werkzeug.utils import redirect
import database.db_access as db
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = '59d3ca27e6701d3fd06eb960ca5866a5'

@app.route("/", methods=["GET"])
@app.route("/home", methods=["GET"])
def home():
    if ('user_id' in session):
        user_name = ", " + db.get_user(session['user_id']).split()[0] + "!"
        return render_template("index.html", log_status="Log Out", user_name=user_name)
    else:
        return render_template("index.html", log_status="Log In")


@app.route("/login", methods=["GET", "POST"])
def login():
    if ('user_id' in session):
        session.clear()
        return render_template("index.html", log_status="Log In")

    data = request.form.to_dict(flat=False)
    print("login data ", data)

    if (data):
        data['email'] = ''.join(data['email'])
        data['password'] = ''.join(data['password'])

        response = db.validate_users(**data)

        if (response is not "invalid"):
            session['user_id'] = response[0]
            user_name = ", " + response[1].split()[0] + "!"
            print("response ", response)
            return render_template("index.html", log_status="Log Out", user_name=user_name)
        flash("invalid email or password")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    data = request.form.to_dict(flat=False)

    print("register data ", data)
    if (data):
        data['name'] = ''.join(data['name'])
        data['email'] = ''.join(data['email'])
        data['password'] = ''.join(data['password'])

        response = db.register_users(**data)
        if (response):
            return redirect(url_for('login'))
        flash("user Exists")
    return render_template('register.html')


if __name__ == "__main__":
    app.run(debug=True, threaded=True)