import time

import pytest
import requests

from TestData.config import idBaseUrl, user_id, client_id, client_secret_key


@pytest.mark.skip(reason="need vpn to run the test")
def test_request_otp_by_pipedream():
    time.sleep(5)
    path = "v1/cosmos/oauth/authenticate"
    payload = {
        "scope": "profile email",
        "user_id": "gamoraUser",
        "client_id": "gamora",
        "code_challenge": "VHOBdw3zXYSD4_qJJlsggDzSgThkoaau1YxDwqwctmc",
        "code_challenge_method": "S256",
        "response_type": "code",
        "auth_client": "random"
    }
    response = requests.post(url=idBaseUrl + path, json=payload)
    data = response.json()

    assert response.status_code == 200
    assert data["timestamp"] is not None

@pytest.mark.skip(reason="need vpn to run the test")
def test_request_otp_by_api():
    time.sleep(5)
    path = "v1/cosmos/otp/request"
    payload = {
        "user_id": user_id,
        "client_id": client_id,
        "client_secret_key": client_secret_key
    }
    response = requests.post(url=idBaseUrl + path, json=payload)
    data = response.json()

    assert response.status_code == 200
    assert data["user_id"] is not user_id
    assert data["otp"] is not None
    return data["otp"]

@pytest.mark.skip(reason="need vpn to run the test")
def test_validate_otp():
    path = "v1/cosmos/oauth/authenticate/validate"
    payload = {
        "user_id": user_id,
        "otp": test_request_otp_by_api(),
        "client_id": client_id
    }
    response = requests.post(url=idBaseUrl + path, json=payload)
    data = response.json()

    assert response.status_code == 200
    assert data["auth_code"] is not None
    return data["auth_code"]

@pytest.mark.skip(reason="need vpn to run the test")
def test_request_token():
    auth_code = test_validate_otp()
    path = "v1/cosmos/oauth/token"
    payload = {
        "auth_code": auth_code,
        "client_id": client_id,
        "code_verifier": "some-code-challenge"
    }
    response = requests.post(url=idBaseUrl + path, json=payload)
    data = response.json()

    assert response.status_code == 200
    assert data["user_id"] == user_id
    assert data["access_token"] is not None
    assert data["refresh_token"] is not None
    return data["access_token"], data["refresh_token"]
