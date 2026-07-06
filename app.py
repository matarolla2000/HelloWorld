from flask import Flask, request, make_response, render_template

app = Flask(__name__)

@app.route("/")
def main():
    username = request.cookies.get("login")
    return render_template("index.html", login=username)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        login_val = data['login']
        password = data['password']
        resp = make_response(render_template('Yandex.html', login=login_val))
        resp.set_cookie("login", login_val)
        return resp
    return render_template("login.html", login=None)

app.run(debug=True)