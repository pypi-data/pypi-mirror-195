import requests
import logging

# from request import Request
from . import request_client

logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self, base_url, auth=None):
        self.base_url = base_url
        self.auth = auth

    def get(self, path=None):
        url = self.base_url + path
        headers = self._get_headers()
        response = request_client.Request(
            "GET", url, headers=headers, auth=self.auth
        ).send()
        return response.json(), response.status_code, response.headers

    def post(self, data, path=None):
        url = self.base_url + path
        headers = self._get_headers()
        response=request_client.Request(
            "POST", url, headers=headers, auth=self.auth, json=data
        ).send()

        return response.json(), response.status_code, response.headers

    def put(self, data, path=None):
        url = self.base_url + path
        headers = self._get_headers()
        response=request_client.Request(
            "PUT", url, headers=headers, auth=self.auth, json=data
        ).send()
        return response.json(), response.status_code, response.headers

    def patch(self, data, path=None):
        url = self.base_url + path
        headers = self._get_headers()
        response=request_client.Request(
            "PATCH", url, headers=headers, auth=self.auth, json=data
        ).send()
        return response.json(), response.status_code, response.headers

    def delete(self, path=None):
        url = self.base_url + path
        headers = self._get_headers()
        response=request_client.Request(
            "DELETE", url, headers=headers, auth=self.auth
        ).send()
        return response.json(), response.status_code, response.headers

    def _get_headers(self):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.auth:
            headers["Authorization"] = "Bearer " + self.auth.token
        return headers
