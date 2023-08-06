#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    session,
    url_for,
)
from werkzeug.security import check_password_hash

from pmml_ui.auth.db import UserDB
from pmml_ui.auth.forms import LoginForm

blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@blueprint.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = UserDB().get_user(username=user_id)


@blueprint.route("/login", methods=("GET", "POST"))
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        error = None
        user = UserDB().get_user(username=username)

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user.password_hash, password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session["user_id"] = user.name
            return redirect(url_for("mailing_lists.index"))

        flash(error)

    return render_template("auth/login.html", login_form=login_form)


@blueprint.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
