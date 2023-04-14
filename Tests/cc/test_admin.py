import pytest as pytest
import requests

from TestData.config import ccBaseUrl, account_id
from conftest import payload_with_file
@pytest.mark.tags("sqecc", "integration")
# @pytest.mark.sqecc
def test_admin_login_successfully():
    path = "v1/agent/login"
    payload = {
        "username": "admin@smma.id",
        "password": "admin"
    }
    response = requests.post(url=ccBaseUrl + path, json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["token"] is not None

@pytest.mark.tags("sqecc", "integration")
# @pytest.mark.sqecc
def test_get_all_account(get_admin_token):
    path = "v1/account"
    headers = {
        "Authorization": "jwt " + get_admin_token
    }
    response = requests.get(url=ccBaseUrl + path, headers=headers)
    assert response.status_code == 200

@pytest.mark.tags("sqecc", "integration")
# @pytest.mark.sqecc
@pytest.mark.parametrize("file_path", ["JsonFile/user.json"])
def test_create_inbox_success(payload_with_file, file_path, get_admin_token):
    path = "v1/account/" + account_id + "/web-widget/inboxes"
    payload = payload_with_file(file_path)

    headers = {
        "Authorization": "jwt " + get_admin_token
    }
    response = requests.post(url=ccBaseUrl + path, headers=headers, json=payload)
    assert response.status_code == 201
