#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.parse


class MailingListMember:
    def __init__(self, address, name=None):
        self.name = name
        self.address = address
        if name is None:
            self.name = self.address.replace("@", "_at_")
            self.name = urllib.parse.quote_plus(self.name)

    def __repr__(self):
        return self.address


class MailingList:
    def __init__(self, address, members, name=None):
        self.name = name
        self.address = address
        self.members = members
        if name is None:
            self.name = self.address.split("@")[0]

    def get_member(self, address):
        for member in self.members:
            if member.address == address:
                return member

    def add_member(self, address):
        member = MailingListMember(address=address)
        self.members.append(member)

    def remove_member(self, address, address_is_url_encoded=True):
        decoded_address = address
        if address_is_url_encoded:
            decoded_address = urllib.parse.unquote_plus(address)
        member = self.get_member(address=decoded_address)
        self.members.remove(member)
