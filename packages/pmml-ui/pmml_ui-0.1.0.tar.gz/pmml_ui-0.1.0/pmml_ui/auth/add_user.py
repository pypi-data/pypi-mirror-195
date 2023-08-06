#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getpass

from pmml_ui.auth.db import UserDB


def add_user():
    user_db = UserDB()
    username = input("User: ")
    password = getpass.getpass("Password: ")
    verify = getpass.getpass("Repeat password: ")
    if password != verify:
        print("Passwords do not match!")
    else:
        user_db.add_user(username, password)
        print("User added.")


if __name__ == "__main__":
    try:
        add_user()
    except KeyboardInterrupt:
        pass
