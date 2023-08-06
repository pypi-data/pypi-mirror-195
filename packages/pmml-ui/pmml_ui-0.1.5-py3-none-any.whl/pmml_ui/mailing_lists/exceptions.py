#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import abort

from pmml_ui.updater import exceptions


def exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exceptions.KubernetesConnectionError:
            return abort(503, "Kubernetes connection failed")

    return inner_function
