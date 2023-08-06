#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pathlib import Path

SECRET_KEY = os.urandom(64)
DEFAULT_USER_FILE_PATH = f"{Path.home()}/.config/pmml-ui/users.json"
USER_FILE_PATH = Path(os.environ.get("PMML_USER_FILE_PATH", DEFAULT_USER_FILE_PATH))
K8S_CONNECTION_TYPE = os.environ.get("PMML_K8S_CONNECTION_TYPE", "local")
