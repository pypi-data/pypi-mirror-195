#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import json
import re

from kubernetes import client, config

from pmml_ui.config import K8S_CONNECTION_TYPE

CONNECTION_TYPE_LOCAL = "local"
CONNECTION_TYPE_INCLUSTER = "incluster"


class JsonSecret:
    def __init__(self, name, namespace, secret, data_path):
        self._data_path = data_path
        self._api_v1_secret = secret
        self._decoded_secret_data = base64.b64decode(secret.data[data_path])
        self._encoded_secret_data = secret.data[data_path]
        self.name = name
        self.namespace = namespace
        self.data = json.loads(self._decoded_secret_data)

    def update(self):
        self._decoded_secret_data = json.dumps(self.data)
        self._encoded_secret_data = base64.b64encode(
            self._decoded_secret_data.encode()
        ).decode("utf-8")
        self._api_v1_secret.data[self._data_path] = self._encoded_secret_data


class Pod:
    def __init__(self, name, namespace):
        self.name = name
        self.namespace = namespace


class Client:
    def __init__(self, connection_type=K8S_CONNECTION_TYPE):
        self.connection_type = connection_type
        self.api_v1 = self.setup(connection_type)

    @staticmethod
    def setup(connection_type):
        if connection_type == CONNECTION_TYPE_LOCAL:
            config.load_kube_config()
        elif connection_type == CONNECTION_TYPE_INCLUSTER:
            config.load_incluster_config()
        return client.CoreV1Api()

    def read_json_secret(self, name, namespace, data_path):
        k8s_secret = self.api_v1.read_namespaced_secret(name, namespace)
        return JsonSecret(name, namespace, k8s_secret, data_path)

    def replace_json_secret(self, secret):
        return self.api_v1.replace_namespaced_secret(
            secret.name, secret.namespace, secret._api_v1_secret
        )

    def delete_pod(self, name, namespace):
        self.api_v1.delete_namespaced_pod(name, namespace)

    def delete_matching_pods_in_namespace(self, namespace, pattern):
        pods_in_namespace = self.api_v1.list_namespaced_pod(namespace)
        compiled_pattern = re.compile(pattern)
        for pod in pods_in_namespace.items:
            if compiled_pattern.match(pod.metadata.name):
                self.delete_pod(pod.metadata.name, namespace)
