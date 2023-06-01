from pydantic import BaseModel
import pytest
import requests


class AccessTokenRequest(BaseModel):
    access_token: str

class User(BaseModel):
    id: int
    first_name: str
    last_name: str


def test_access_token_required():
    request = {
        "access_token": "token1234"
    }
    AccessTokenRequest(**request)


def test_users_get_response():
    response = [
        {"id": 1234, "first_name": "Jo", "last_name": "Leto"},
        {"id": 5678, "first_name": "Ja", "last_name": "Leto"}
    ]
    users = [User(**user) for user in response]



def test_access_token_required():
    request = {}
    with pytest.raises(ValueError):
        AccessTokenRequest(**request)


def test_access_token_format():
    request = {
        "access_token": "invalid_token_format"
    }
    with pytest.raises(ValueError):
        AccessTokenRequest(**request)


def test_users_get_success():
    response = [
        {"id": 1234, "first_name": "Jo", "last_name": "Leto"},
        {"id": 5678, "first_name": "Ja", "last_name": "Leto"}
    ]
    users = [User(**user) for user in response]
    assert len(users) == 2
    assert users[0].id == 123
    assert users[0].first_name == "John"
    assert users[0].last_name == "Doe"


def test_users_get_no_users():
    response = []
    users = [User(**user) for user in response]
    assert len(users) == 0


def test_user_format():
    user = {
        "id": "invalid_id_format",
        "first_name": "Jo",
        "last_name": "Leto"
    }
    with pytest.raises(ValueError):
        User(**user)


def test_user_name_format():
    user = {
        "id": 1234,
        "first_name": "Jo1234",
        "last_name": "Leto"
    }
    with pytest.raises(ValueError):
        User(**user)


def test_user_lastname_format():
    user = {
        "id": 1234,
        "first_name": "Jo",
        "last_name": "Leto1234"
    }
    with pytest.raises(ValueError):
        User(**user)


def test_users_get_one_user():
    response = [{"id": 1234, "first_name": "Jo", "last_name": "Leto"}]
    users = [User(**user) for user in response]
    assert len(users) == 1
    assert users[0].id == 1234
    assert users[0].first_name == "Jo"
    assert users[0].last_name == "Leto"



def test_users_get_max_users():
    response = [{"id": i, "first_name": "User", "last_name": str(i)} for i in range(1000)
]
    users = [User(**user) for user in response]
    assert len(users) == 1000
    assert users[-1].id == 999
    assert users[-1].first_name == "User"
    assert users[-1].last_name == "999"


def test_users_get_invalid_response():
    response = [{"invalid_attr": "value"}]
    with pytest.raises(ValueError):
        users = [User(**user) for user in response]