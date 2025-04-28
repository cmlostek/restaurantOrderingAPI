from fastapi.testclient import TestClient
from ..controllers import orders as controller
from ..main import app
import pytest
from ..models import orders as model

# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_new_order(db_session, mocker):

    # mocking function
    mock_create_order = mocker.patch.object(controller, 'create_order', return_value=model.Order(id=1, name="Test Order"))

    # sample order request
    order_request = {
        "user_id": 1,
        "dish_id": 1,
        "name": "Test Order",
        "description": "This is a test order",
        "price": 100.0,
        "quantity": 2
        "is_guest": 1
    }

    # make a post-request to create order
    response = client.post("/orders/", json=order_request)

    # asserting the response for the order
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Test Order", "description": "This is a test order", "price": 100.0, "quantity": 2}

    # assert incorrect order as intended
    response = client.post("/orders/", json={})
    assert response.status_code == 422


def test_read_all_orders(db_session, mocker):

    mock_get_all_orders = mocker.patch.object(controller, 'get_all_orders', return_value=[model.Order(id=1, name="Test Order")])

    response = client.get("/orders/")

    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Test Order"}]

def test_update_existing_order(db_session, mocker):

    mock_update_order = mocker.patch.object(controller, 'update_order', return_value=model.Order(id=1, name="Updated Order"))

    order_update_request = {
        "user_id": 1,
        "dish_id": 1,
        "name": "Updated Order",
        "description": "This is an updated test order",
        "price": 150.0,
        "quantity": 3,
        "is_guest": 1,
    }

    response = client.put("/orders/1", json=order_update_request)

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Updated Order", "description": "This is an updated test order", "price": 150.0, "quantity": 3}

def test_delete_existing_order(db_session, mocker):
    mock_delete_order = mocker.patch.object(controller, 'delete_order', return_value=model.Order(id=1, name="Deleted Order"))

    response = client.delete("/orders/1")

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Deleted Order"}


