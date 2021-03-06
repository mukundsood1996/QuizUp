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


@app.route("/quizzes", methods=["GET"])
def quizzes():
    if ('user_id' in session):
        user_name = ", " + db.get_user(session['user_id']).split()[0] + "!"
        return render_template("quizzes.html", log_status="Log Out", user_name=user_name)
    else:
        return render_template("quizzes.html", log_status="Log In")


@app.route("/about_us", methods=["GET"])
def about_us():
    if ('user_id' in session):
        user_name = ", " + db.get_user(session['user_id']).split()[0] + "!"
        return render_template("about.html", log_status="Log Out", user_name=user_name)
    else:
        return render_template("about.html", log_status="Log In")


@app.route("/contact_us", methods=["GET"])
def contact_us():
    if ('user_id' in session):
        user_name = ", " + db.get_user(session['user_id']).split()[0] + "!"
        return render_template("contact.html", log_status="Log Out", user_name=user_name)
    else:
        return render_template("contact.html", log_status="Log In")


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if 'user_id' in session:
        user_name = ", " + db.get_user(session['user_id']).split()[0] + "!"

        data = request.form.to_dict(flat=False)
        print("\n\n\nQuiz name ", data)

        if (data['quizName'][0] == 'galaxies'):
            quizName = "the Galaxies"
        elif (data['quizName'][0] == 'worldCup'):
            quizName = "the Football World Cup 2018"
        elif (data['quizName'][0] == 'maths'):
            quizName = "the Mathematics"
        elif (data['quizName'][0] == 'cricket'):
            quizName = "the Cricket"
        else:
            quizName = "to create a"

        session['quiz_id'] = db.get_quiz_id(''.join(data['quizName'][0]))
        print("Quiz_id is ", session['quiz_id'])
        return render_template("quiz.html", log_status="Log Out", user_name=user_name, quiz_name=quizName)
    else:
        return render_template("login.html", log_status="Log In")


@app.route("/question", methods=["GET", "POST"])
def question():
    print("Getting questions")
    quiz_id = request.args.get('quiz', 0)

    questions = db.get_questions(quiz_id)
    num_questions = db.get_num_questions(quiz_id)

    all_info = questions + num_questions

    return (jsonify(all_info))


@app.route("/pass_score", methods=['GET'])
def pass_score():
    print("Passing Score")
    score = request.args.get('score', 0)
    user_name = db.get_user_name(session['user_id'])
    response = db.get_leaderboard(session['quiz_id'])
    if (len(response) < db.users_per_quiz_per_leaderboard or
            (response[db.users_per_quiz_per_leaderboard - 1][1] < score and
             user_name not in [i[0] for i in response])):
        request_data = {
            'quiz_id': session['quiz_id'],
            'user_id': session['user_id'],
            'score': score
        }
        print("Hellllll")
        response = db.update_leaderboard(**request_data)
        if (response):
            return "True"
    return "False"


@app.route("/poll_leaderboard", methods=['GET', 'POST'])
def poll_leaderboard():
    print("Polling")
    response = db.get_leaderboard(session['quiz_id'])
    response = dict(response)
    while (True):
        new_response = db.get_leaderboard(session['quiz_id'])
        new_response = dict(new_response)
        shared_items = {k: new_response[k] for k in new_response if k in response and new_response[k] == response[k]}
        if (len(shared_items) > 0):
            print(jsonify(new_response))
            return jsonify(new_response)


@app.route("/get_quiz_names/<prefix>", methods=['GET'])
def get_quiz_names(prefix):
    response = db.get_quiz_names(prefix)
    if (response):
        return render_template("quiz.html", quiz=response)


@app.route("/validate_email", methods=["GET"])
def validate_email():
    request_data = request.args.get('email_id', 0)
    print("Checking for ", request_data)
    response = db.validate_email(request_data)
    print(response)
    return (jsonify(response))

@app.route("/recommend", methods = ["GET"])
def get_recommendations():
    request_data = request.args.get('quiz_name', 0)
    from gensim.test.utils import datapath, get_tmpfile
    from gensim.models import KeyedVectors

    glove_file = datapath('/home/mathuryash5/7th Sem/Web Technologies - II/QuizUp/trained_model/glove.6B.50d.txt')
    tmp_file = get_tmpfile("word2vec_50d.txt")
    # calling glove2word2vec script
    from gensim.scripts.glove2word2vec import glove2word2vec
    glove2word2vec(glove_file, tmp_file)

    model = KeyedVectors.load_word2vec_format(tmp_file)


    res = model.most_similar(request_data, topn=10, restrict_vocab=None)

    return jsonify(res)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)