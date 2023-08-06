#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    from pmml_ui.auth.views import blueprint as auth_blueprint

    app.register_blueprint(auth_blueprint)

    from pmml_ui.mailing_lists.views import blueprint as mailing_lists_blueprint

    app.register_blueprint(mailing_lists_blueprint)
    app.add_url_rule("/", endpoint="mailing_lists.index")

    return app
