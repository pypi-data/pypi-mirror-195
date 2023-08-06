#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, abort, g, redirect, render_template, session, url_for

from pmml_ui.auth.views import login_required
from pmml_ui.config import (
    PMML_NAMESPACE,
    PMML_PMMLRC_FILE_NAME,
    PMML_PMMLRC_SECRET_NAME,
    PMML_POD_BASENAME,
)
from pmml_ui.mailing_lists.exceptions import exception_handler
from pmml_ui.mailing_lists.forms import MailingListForm, MailingListMemberFormCSRF
from pmml_ui.updater.client import ConfigUpdater

blueprint = Blueprint("mailing_lists", __name__, url_prefix="/mailing_lists")


@blueprint.before_app_request
@exception_handler
def setup_updater():
    if "user_id" in session:
        g.updater = ConfigUpdater(
            namespace=PMML_NAMESPACE,
            pod_basename=PMML_POD_BASENAME,
            secret_name=PMML_PMMLRC_SECRET_NAME,
            secret_filename=PMML_PMMLRC_FILE_NAME,
        )


@blueprint.route("/")
@login_required
def index():
    return render_template(
        "mailing_lists/list.html", mailing_lists=g.updater.config.mailing_lists.values()
    )


@blueprint.route("/<mailing_list_name>", methods=["GET", "POST"])
@login_required
def detail(mailing_list_name):
    if mailing_list_name not in g.updater.config.mailing_lists:
        abort(404, description="Resource not found")
    mailing_list = g.updater.config.mailing_lists[mailing_list_name]
    mailing_list_form = MailingListForm(obj=mailing_list)
    if mailing_list_form.validate_on_submit():
        g.updater.config.mailing_lists[
            mailing_list_name
        ] = mailing_list_form.mailing_list
        g.updater.update(mailing_list_form.mailing_list)
        return redirect(
            url_for("mailing_lists.detail", mailing_list_name=mailing_list_name)
        )
    return render_template(
        "mailing_lists/detail.html",
        mailing_list=mailing_list,
        mailing_list_form=mailing_list_form,
    )


@blueprint.route("/<mailing_list_name>/add", methods=["GET", "POST"])
@login_required
def add_member(mailing_list_name):
    if mailing_list_name not in g.updater.config.mailing_lists:
        abort(404, description="Resource not found")
    mailing_list = g.updater.config.mailing_lists[mailing_list_name]
    member_form = MailingListMemberFormCSRF()
    if member_form.validate_on_submit():
        mailing_list.add_member(address=member_form.address.data)
        g.updater.update(mailing_list)
        return redirect(
            url_for("mailing_lists.detail", mailing_list_name=mailing_list_name)
        )
    return render_template(
        "mailing_lists/add_member.html",
        member_form=member_form,
        mailing_list_name=mailing_list.name,
    )


@blueprint.route("/<mailing_list_name>/<member_address>/delete")
@login_required
def delete_member(mailing_list_name, member_address):
    if mailing_list_name not in g.updater.config.mailing_lists:
        abort(404, description="Resource not found")
    mailing_list = g.updater.config.mailing_lists[mailing_list_name]
    if mailing_list.get_member(member_address) is None:
        abort(404, description="Resource not found")
    mailing_list.remove_member(member_address)
    g.updater.update(mailing_list)
    return redirect(
        url_for("mailing_lists.detail", mailing_list_name=mailing_list_name)
    )
