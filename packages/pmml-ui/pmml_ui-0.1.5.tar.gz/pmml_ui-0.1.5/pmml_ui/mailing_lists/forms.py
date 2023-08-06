#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import FieldList, Form, FormField, HiddenField, StringField
from wtforms.validators import DataRequired, Email

from pmml_ui.mailing_lists.models import MailingList, MailingListMember


class MailingListMemberForm(Form):
    name = HiddenField("name")
    address = StringField("address", validators=[DataRequired(), Email()])


class MailingListMemberFormCSRF(FlaskForm):
    name = HiddenField("name")
    address = StringField("address", validators=[DataRequired(), Email()])


class MailingListForm(FlaskForm):
    name = HiddenField("name")
    address = StringField("address", validators=[DataRequired(), Email()])
    members = FieldList(FormField(MailingListMemberForm))

    @property
    def mailing_list(self):
        member_objects = [
            MailingListMember(address=member.address.data) for member in self.members
        ]
        return MailingList(address=self.address.data, members=member_objects)
