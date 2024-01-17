from flask import request, session, redirect, url_for, render_template, flash
from app.auth import bp
from app.extensions import mysql

from werkzeug.security import generate_password_hash, check_password_hash
import hashlib

def login_required(view):
    import functools
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get("userID") is None:
            session["redirectUrl"] = request.url
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


@bp.route('/')
def index():
    user = session.get("userID")
    return f'''UserID: {user}<br>
    <a href="/auth/login">Login</a><br>
    <a href="/auth/logout">Logout</a><br>
    <a href="/auth/regestration">Regestration</a><br>
    <a href="/">Main</a>'''


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        datafields = ["email","password"]
        if len(data) != 3:
            return render_template("auth/login.html"), 400
        for item in datafields:
            if data.get(item) == None:
                return render_template("auth/login.html"), 400
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT `userID`,`hash`,`verified` FROM user WHERE email = %s", (data.get("email"),))
        result = cursor.fetchone()
        if result == None:
            flash("Check deine Eingabe!", "info")
            return render_template("auth/login.html"), 401   
        if not check_password_hash(result[1], data.get("password")):
            flash("Check deine Eingabe!", "info")
            return render_template("auth/login.html"), 401
        if result[2] == 0:
            # TODO sende eine Mail mit aktivierungs url
            flash("Bitte aktiviere zuerst dein Konto!", "info")
            return render_template("auth/login.html"), 401
        session["userID"] = result[0]
        if session.get("redirectUrl"):
            next_url = session.pop("redirectUrl", None)
            return redirect(next_url)

        return redirect(url_for("auth.index"))
    return render_template("auth/login.html")


@bp.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("auth.index"))


@bp.route("/registration", methods=["GET", "POST"])
def registration():
    session.clear()
    if request.method == "POST":
        data = request.form
        datafields = ["lastname","firstname","username","email","password"]
        if len(data) != 6:
            return render_template("auth/registration.html"), 400
        for item in datafields:
            if data.get(item) == None:
                return render_template("auth/registration.html"), 400
        cursor = mysql.connection.cursor()
        cursor.execute(f"SELECT `userID` FROM user WHERE email = '{data.get("email")}'")
        result = cursor.fetchone()
        cursor.close()
        if result is not None:
            # TODO sende eine Mail
            flash("Dein Konto wurde angelegt, schau in deinem Posteingang!", "info")
            return redirect(url_for("auth.login"))
        hash = generate_password_hash(data.get("password"))
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO user (`firstname`,`lastname`,`username`,`email`,`hash`,`userGroupID`,`languageID`) VALUES (%s,%s,%s,%s,%s,%s,%s)", 
                       (data.get("firstname"),data.get("lastname"),data.get("username"),data.get("email"), hash, 2, 1))
        mysql.connection.commit()
        cursor.execute(f"SELECT `userID` FROM user WHERE email = '{data.get("email")}'")
        result = str(cursor.fetchone()[0])
        url = hashlib.sha256(result.encode()).hexdigest()
        cursor.execute("INSERT INTO userVerified (`userID`,`url`) VALUES (%s,%s)", 
                       (result, url))
        mysql.connection.commit()
        cursor.close()
        # TODO sende eine Mail mit aktivierungs url
        flash("Dein Konto wurde angelegt, schau in deinem Posteingang!", "info")
        return redirect(url_for("auth.login"))
    return render_template("auth/registration.html")


@bp.route("/verifie/<url>", methods=["GET"])
def verifie(url):
    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT `userID` FROM userVerified WHERE url = '{url}'")
    result = cursor.fetchone()
    if result == None:
        return redirect(url_for("auth.index")), 401
    cursor.execute(f"UPDATE `user` SET `verified` = 1 WHERE userID = '{result[0]}'")
    mysql.connection.commit()
    cursor.execute(f"DELETE FROM `userVerified` WHERE url = '{url}'")
    mysql.connection.commit()
    cursor.close()
    flash("Konto wurde aktiviert!", "info")
    return redirect(url_for("auth.index"))

