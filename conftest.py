import json
import os.path

import pytest
import requests

from TestData.config import ccBaseUrl


@pytest.fixture()
def get_admin_token():
    path = "v1/agent/login"
    payload = {
        "username": "admin@smma.id",
        "password": "admin"
    }
    response = requests.post(url=ccBaseUrl + path, json=payload)
    assert response.status_code == 200

    data = response.json()
    jwt_token = data["token"]
    return jwt_token


@pytest.fixture
def payload_with_file():
    def _payload_with_file(file_path):
        dir_name = os.path.dirname(__file__)
        file_name = os.path.join(dir_name, file_path)
        with open(file_name, 'r') as f:
            payload = json.load(f)
            return payload

    return _payload_with_file
