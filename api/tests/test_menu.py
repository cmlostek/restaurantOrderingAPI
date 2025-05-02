from fastapi.testclient import TestClient
from prompt_toolkit.widgets import MenuItem

from ..controllers import orders as controller
from ..main import app
import pytest
from ..models import orders as model

# Create a test client for the app
client = TestClient(app)


@pytest.fixture(scope='module')
def seeded_client():
    return client

def test_get_menu_list(seeded_client):
    response = seeded_client.get('/menu/')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(item['dish_id'] == 1 for item in data)


def test_read_menu_item_by_id(seeded_client):
    response = seeded_client.get('/menu/1')
    assert response.status_code == 200
    data = response.json()
    assert data['dish_id'] == 1
    assert data['dish'] == "Margherita Pizza"
    assert data['price'] == 10.5
    assert data['calories'] == 700
    assert data['category'] == "Pizza"
    assert isinstance(data['ingredients'], list)


def test_create_menu_item(seeded_client):
    menu_request = {
        "dish_id": 5,
        "dish": "Pepperoni Pizza",
        "price": 12.0,
        "ingredients": [1, 2],
        "calories": 1000,
        "category": "Pizza"
    }

    response = seeded_client.post('/menu/', json=menu_request)
    assert response.status_code == 200
    data = response.json()
    assert data['dish_id'] == 5
    assert data['dish'] == "Pepperoni Pizza"
    assert data['price'] == 12.0
    assert data['calories'] == 1000
    assert data['category'] == "Pizza"
    assert isinstance(data['ingredients'], list)

def test_update_menu_item(seeded_client):
    menu_update_request = {
        "dish_id": 1,
        "dish": "Margherita Pizza - New Recipe",
        "price": 11.50,
        "ingredients": [1, 3, 7],
        "calories": 900,
        "category": "Pizza"
    }

    response = seeded_client.put('/menu/1', json=menu_update_request)
    assert response.status_code == 200
    data = response.json()
    assert data['dish_id'] == 1
    assert data['dish'] == "Margherita Pizza - New Recipe"
    assert data['price'] == 11.50
    assert data['calories'] == 900
    assert data['category'] == "Pizza"
    assert isinstance(data['ingredients'], list)

def test_delete_menu_item(seeded_client):
    temp_menu = {
        "dish_id": 999,
        "dish": "Temp Dish",
        "price": 1.00,
        "ingredients": [1],
        "calories": 100,
        "category": "Test"
    }
    create_resp = seeded_client.post("/menu/", json=temp_menu)
    assert create_resp.status_code == 200

    del_resp = seeded_client.delete("/menu/999")
    assert del_resp.status_code == 200
    data = del_resp.json()
    assert data["dish_id"] == 999
    assert data["dish"] == "Temp Dish"

    get_resp = seeded_client.get("/menu/999")
    assert get_resp.status_code == 404

