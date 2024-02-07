from flask import Blueprint, render_template, request, redirect, session, url_for, abort
import hashlib
import os

auth_blueprint = Blueprint("auth", __name__, template_folder="templates")


def is_granted():
    if not "access" in session:
        abort(redirect(url_for("auth.login")))


@auth_blueprint.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        password = request.form["password"]
        md5password = str(os.environ.get('PASSWORD', "bea79cf8098f4f9b3cc376e52ea98401"))
        if(hashlib.md5(password.encode('utf-8')).hexdigest() == md5password):
            session["access"] = True
            return redirect(url_for("auth.login"))
    else:
        if "access" in session:
            return redirect(url_for("home"))

        return render_template("login.html")
    return render_template("login.html")


@auth_blueprint.route("/logout")
def logout():
    session.pop("access", None)
    return redirect(url_for("auth.login"))


