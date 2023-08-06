#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pathlib import Path

from werkzeug.security import generate_password_hash

from pmml_ui.auth.models import User
from pmml_ui.config import USER_FILE_PATH


class UserDB:
    def __init__(self, user_file_path=USER_FILE_PATH):
        self.file_path = Path(user_file_path)
        self.users = self.load()

    def load(self):
        if self.file_path.exists():
            with open(self.file_path) as users_file:
                users = json.load(users_file)
        else:
            users = {}
        return users

    def get_user(self, username):
        user = None
        if username in self.users:
            user = User(
                name=username, password_hash=self.users[username]["password_hash"]
            )
        return user

    def save(self):
        with open(self.file_path, "w") as users_file:
            json.dump(self.users, users_file)

    def add_user(self, username, password):
        password_hash = generate_password_hash(password)
        if username in self.users:
            raise KeyError("User already exists.")
        self.users[username] = {"password_hash": password_hash}
        self.save()
