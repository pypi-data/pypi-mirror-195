#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pmml_ui.mailing_lists.models import MailingList, MailingListMember


class PmmlConfiguration:
    def __init__(self, json_secret):
        self.json_secret = json_secret
        self.mailing_lists = self.read_mailing_lists_from_json(self.json_secret)

    def read_mailing_lists_from_json(self, json_secret):
        mailing_lists = {}
        for mailing_list_address in json_secret.data:
            members = []
            for member_address in json_secret.data[mailing_list_address]["recipients"]:
                member = MailingListMember(address=member_address)
                members.append(member)
            mailing_list = MailingList(address=mailing_list_address, members=members)
            mailing_lists[mailing_list.name] = mailing_list
        return mailing_lists

    def update(self, mailing_list):
        recipients = [member.address for member in mailing_list.members]
        self.json_secret.data[mailing_list.address]["recipients"] = recipients
        self.json_secret.update()
