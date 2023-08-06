#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib3.exceptions import MaxRetryError


class KubernetesConnectionError(Exception):
    pass


def exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except MaxRetryError:
            raise KubernetesConnectionError("Connection failed")

    return inner_function
