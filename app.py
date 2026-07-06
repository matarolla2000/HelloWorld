from flask import Flask, request, make_response, render_template

app = Flask(__name__)

@app.route("/")
def main():
    pass

@app.route("/login", methods="POST")
def login():
    data = request.form
    login = data['login']
    resp = make_response(render_template('index.html', login=login))
    resp.set_cookie("login", login)
    return render_template("login.html", login=login)