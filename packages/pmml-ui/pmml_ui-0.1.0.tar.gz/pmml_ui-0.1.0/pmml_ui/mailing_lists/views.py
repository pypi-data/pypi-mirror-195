#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, g, redirect, render_template, url_for

from pmml_ui.auth.views import login_required
from pmml_ui.mailing_lists.forms import MailingListForm, MailingListMemberFormCSRF
from pmml_ui.updater.client import ConfigUpdater

blueprint = Blueprint("mailing_lists", __name__, url_prefix="/mailing_lists")


@blueprint.before_app_request
def setup_updater():
    g.updater = ConfigUpdater("pmml", "pmml-deployment", "pmml-pmmlrc", ".pmmlrc")


@blueprint.route("/")
@login_required
def index():
    return render_template(
        "mailing_lists/list.html", mailing_lists=g.updater.config.mailing_lists.values()
    )


@blueprint.route("/<mailing_list_name>", methods=["GET", "POST"])
@login_required
def detail(mailing_list_name):
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
    mailing_list = g.updater.config.mailing_lists[mailing_list_name]
    mailing_list.remove_member(member_address)
    g.updater.update(mailing_list)
    return redirect(
        url_for("mailing_lists.detail", mailing_list_name=mailing_list_name)
    )
