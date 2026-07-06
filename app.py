from functools import wraps

from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config["SECRET_KEY"] = "change-me-to-a-random-secret-value"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)


with app.app_context():
    db.create_all()


def login_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("register"))
        return view_func(*args, **kwargs)
    return wrapped


@app.route("/")
@login_required
def main():
    return render_template("index.html", login=session.get("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        login_val = request.form.get("login", "").strip()
        password = request.form.get("password", "")

        if not login_val or not password:
            flash("Заполните логин и пароль")
            return render_template("register.html")

        user = User.query.filter_by(login=login_val).first()

        if user:
            # Логин уже существует — проверяем пароль (это вход)
            if not check_password_hash(user.password_hash, password):
                flash("Неверный пароль для этого логина")
                return render_template("register.html")
        else:
            # Логина ещё нет — создаём новый аккаунт (это регистрация)
            user = User(login=login_val, password_hash=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()

        session["user_id"] = user.id
        session["login"] = user.login
        return redirect(url_for("main"))

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("register"))


if __name__ == "__main__":
    app.run(debug=True)
