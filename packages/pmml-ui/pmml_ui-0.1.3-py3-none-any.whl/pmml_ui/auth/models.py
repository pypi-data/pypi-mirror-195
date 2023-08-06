#!/usr/bin/env python
# -*- coding: utf-8 -*-


class User:
    def __init__(self, name, password_hash):
        self.name = name
        self.password_hash = password_hash
