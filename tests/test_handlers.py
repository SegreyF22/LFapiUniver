import json
from uuid import uuid4

import pytest


# @pytest.mark.asyncio
async def test_create_user(client, get_user_from_database):
    user_data = {
        "name": "Egor",
        "surname": "Gaidar",
        "email": "raketa@most.com"
    }
    resp = client.post("/user/", data=json.dumps(user_data))
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["name"] == user_data["name"]
    assert data_from_resp["surname"] == user_data["surname"]
    assert data_from_resp["email"] == user_data["email"]
    assert data_from_resp["is_active"] is True
    users_from_db = await get_user_from_database(data_from_resp["user_id"])
    assert len(users_from_db) == 1
    users_from_db = dict(users_from_db[0])
    assert users_from_db["name"] == user_data["name"]
    assert users_from_db["surname"] == user_data["surname"]
    assert users_from_db["email"] == user_data["email"]
    assert users_from_db["is_active"] is True
    assert str(users_from_db["user_id"]) == data_from_resp["user_id"]


async def test_delete_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Egor",
        "surname": "Gaidar",
        "email": "raketa@most.com",
        "is_active": True
    }
    await create_user_in_database(**user_data)
    resp = client.delete(f"/user/?user_id={user_data['user_id']}")
    assert resp.status_code == 200
    assert resp.json() == {"deleted_user_id": str(user_data["user_id"])}
    users_from_db = await get_user_from_database(user_data["user_id"])
    users_from_db = dict(users_from_db[0])
    assert users_from_db["name"] == user_data["name"]
    assert users_from_db["surname"] == user_data["surname"]
    assert users_from_db["email"] == user_data["email"]
    assert users_from_db["is_active"] is False
    assert users_from_db["user_id"] == user_data["user_id"]


async def test_get_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Egor",
        "surname": "Gaidar",
        "email": "raketa@most.com",
        "is_active": True
    }
    await create_user_in_database(**user_data)
    resp = client.get(f"/user/?user_id={user_data['user_id']}")
    assert resp.status_code == 200
    user_from_response = resp.json()
    assert user_from_response["user_id"] == str(user_data["user_id"])
    assert user_from_response["name"] == user_data["name"]
    assert user_from_response["surname"] == user_data["surname"]
    assert user_from_response["email"] == user_data["email"]
    assert user_from_response["is_active"] == user_data["is_active"]


async def test_update_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Egor",
        "surname": "Gaidar",
        "email": "raketa@most.com",
        "is_active": True
    }
    user_data_updated = {
        "name": "Ivan",
        "surname": "Ivanich",
        "email": "Ivanov@.com",
    }
    await create_user_in_database(**user_data)
    resp = client.patch(f"/user/?user_id={user_data['user_id']}", data=json.dumps(user_data_updated))
    assert resp.status_code == 200
    resp_data = resp.json()
    assert resp_data["updated_user_id"] == str(user_data["user_id"])
    users_from_db = await get_user_from_database(user_data["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data_updated["name"]
    assert user_from_db["surname"] == user_data_updated["surname"]
    assert user_from_db["email"] == user_data_updated["email"]
    assert user_from_db["is_active"] is user_data_updated["is_active"]
    assert user_from_db["user_id"] == user_data_updated["user_id"]


# @pytest.mark.parametrize("user_data_updated, expected_status_code, expected_detail", [
#     ({}, 422, {"detail": "At least one parameter for user update info should bo provided"}),
#
# ])
