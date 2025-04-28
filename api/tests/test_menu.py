from fastapi.testclient import TestClient
from prompt_toolkit.widgets import MenuItem

from ..controllers import orders as controller
from ..main import app
import pytest
from ..models import orders as model

# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()

def test_read_all_menu_items(db_session, mocker):
    mock_get_all_menu_items = mocker.patch.object(controller, 'read_all_menu_items', return_value=[MenuItem(id=1, name="Test Menu")])

    response = client.get("/menu/")

    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Test Menu"}]


def test_read_menu_item_by_id(db_session, mocker):
    mock_get_menu_item_by_id = mocker.patch.object(controller, 'read_menu_item_by_id', return_value=MenuItem(id=1, name="Test Menu"))

    response = client.get("/menu/1")

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Test Menu"}


def test_create_new_menu_item(db_session, mocker):
    mock_create_menu_item = mocker.patch.object(controller, 'create_new_menu_item', return_value=MenuItem(id=1, name="Test Menu"))

    menu_request = {
        "name": "Test Menu",
        "description": "This is a test menu",
        "price": 100.0,
        "category": "Test Category"
    }

    response = client.post("/menu/", json=menu_request)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Test Menu"}

def test_update_existing_menu_item(db_session, mocker):
    mock_update_menu_item = mocker.patch.object(controller, 'update_existing_menu_item', return_value=MenuItem(id=1, name="Updated Menu"))

    menu_request = {
        "menu_id": 1,
        "name": "Updated Test Menu",
        "description": "This is an updated test menu",
        "price": 150.0,
        "category": "Updated Category"
    }

    response = client.put("/menu/1", json=menu_request)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Updated Menu"}

def test_delete_menu_item(db_session, mocker):
    mock_delete_menu_item = mocker.patch.object(controller, 'delete_menu_item', return_value=True)

    response = client.delete("/menu/1")

    assert response.status_code == 200
    assert response.json() == {"message": "Menu item deleted successfully"}


