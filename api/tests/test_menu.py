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

@pytest.mark.order(1)
def test_get_menu_list(seeded_client):
    response = seeded_client.get('/menu/')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(item['dish_id'] == 1 for item in data)


@pytest.mark.order(2)
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


@pytest.mark.order(3)
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
        "dish_id": 5,
        "dish": "Pepperoni Pizza - New Recipe",
        "price": 11.50,
        "ingredients": [1, 3],
        "calories": 900,
        "category": "Pizza"
    }

    response = seeded_client.put('/menu/5', json=menu_update_request)
    assert response.status_code == 200
    data = response.json()
    assert data['dish_id'] == 5
    assert data['dish'] == "Pepperoni Pizza - New Recipe"
    assert data['price'] == 11.50
    assert data['calories'] == 900
    assert data['category'] == "Pizza"
    assert isinstance(data['ingredients'], list)

@pytest.mark.order(4)
def test_delete_menu_item(seeded_client):
    response = seeded_client.delete('/menu/5')
    assert response.status_code == 200
    data = response.json()
    print(data, "here")
    assert data == {
                    "dish_id": 5,
                   "dish": "Pepperoni Pizza - New Recipe",
                   "price": 11.5, "ingredients": [1,3],
                   "calories": 900,
                   "category": "Pizza"
                }


    response = seeded_client.get('/menu/5')
    assert response.status_code == 404

