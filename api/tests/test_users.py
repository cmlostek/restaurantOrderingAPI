from fastapi.testclient import TestClient
from ..controllers import orders as controller
from ..main import app
import pytest
from ..models import orders as model

# Create a test client for the app
client = TestClient(app)



@pytest.fixture(scope='module')
def seeded_client():
    return client


def test_read_all_users(seeded_client):
    response = seeded_client.get('/users/')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(user['user_id'] == 1 for user in data)


def test_read_user_by_id(seeded_client):
    response = seeded_client.get('/users/1')
    assert response.status_code == 200
    data = response.json()
    assert data == {
        "user_id": 1,
        "user_name": "alice_w",
        "email": "alice@example.com",
        "phone_number": "5551234567",
        "address": "123 Garden Ave",
        "user_role": "customer",
        "payment_info": "card",
        "review": "Loved the Chicken Alfredo!",
        "rating": "5"
    }


def test_create_new_user(seeded_client):
    new_user = {
        "user_id": 999,
        "user_name": "test_user",
        "email": "test@example.com",
        "phone_number": "1234567890",
        "address": "100 Test St Test City",
        "user_role": "customer",
        "payment_info": "card",
        "review": None,
        "rating": None
    }

    response = seeded_client.post('/users/', json=new_user)
    assert response.status_code == 200
    data = response.json()
    assert data == {
        "user_id": 999,
        "user_name": "test_user",
        "email": "test@example.com",
        "phone_number": "1234567890",
        "address": "100 Test St Test City",
        "user_role": "customer",
        "payment_info": "card",
        "review": None,
        "rating": None
    }

def test_update_existing_user(seeded_client):
    update_data = {
        "user_id": 1,
        "user_name": "alice_w",
        "email": "alice@example.com",
        "phone_number": "5551234567",
        "address": "123 Garden Ave",
        "user_role": "customer",
        "payment_info": "card",
        "review": "Hated the Chicken Alfredo!",
        "rating": "5"
    }
    response = seeded_client.put('/users/1', json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data == {
        "user_id": 1,
        "user_name": "alice_w",
        "email": "alice@example.com",
        "phone_number": "5551234567",
        "address": "123 Garden Ave",
        "user_role": "customer",
        "payment_info": "card",
        "review": "Hated the Chicken Alfredo!",
        "rating": "5"
    }

def test_delete_existing_user(seeded_client):
    temp_user = {
        "user_id": 999,
        "user_name": "updated_user",
        "email": "updated@example.com",
        "phone_number": "9876543210",
        "address": "200 Updated Ave",
        "user_role": "customer",
        "payment_info": "paypal",
        "review": "Great service",
        "rating": "5"
    }

    create_resp = seeded_client.post("/users/", json=temp_user)
    assert create_resp.status_code == 200

    del_resp = seeded_client.delete("/users/999")
    assert del_resp.status_code == 200
    data = del_resp.json()
    assert data["detail"] == "User deleted successfully"












