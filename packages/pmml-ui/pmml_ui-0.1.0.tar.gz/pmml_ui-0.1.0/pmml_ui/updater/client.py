#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pmml_ui.updater.k8s import Client, Pod
from pmml_ui.updater.models import PmmlConfiguration


class ConfigUpdater:
    def __init__(self, namespace, pod_name, secret_name, secret_filename):
        self.client = Client()
        secret = self.client.read_json_secret(secret_name, namespace, secret_filename)
        self.config = PmmlConfiguration(secret)
        self.pod = Pod(pod_name, namespace)

    def update(self, mailing_list):
        pod_pattern = f"^{self.pod.name}-.*$"
        self.config.update(mailing_list)
        self.client.replace_json_secret(self.config.json_secret)
        self.client.delete_matching_pods_in_namespace(
            pattern=pod_pattern, namespace=self.pod.namespace
        )

    def refresh(self):
        secret = self.client.read_json_secret(
            self.config.json_secret.name,
            self.config.json_secret.namespace,
            self.config.json_secret._data_path,
        )
        self.config = PmmlConfiguration(secret)
