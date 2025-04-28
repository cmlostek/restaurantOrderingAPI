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


def test_get_order_details(db_session, mocker):
    mock_get_all_order_details = mocker.patch.object(controller, 'get_all_order_details', return_value=[model.OrderDetail(id=1, order_id=1, dish_id=1, quantity=2)])
    response = client.get("/orders/1/details/")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "order_id": 1, "dish_id": 1, "quantity": 2}]

def test_get_order_detail_by_id(db_session, mocker):
    mock_get_order_detail_by_id = mocker.patch.object(controller, 'get_order_detail_by_id', return_value=model.OrderDetail(id=1, order_id=1, dish_id=1, quantity=2))
    response = client.get("/orders/1/details/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "order_id": 1, "dish_id": 1, "quantity": 2}

def test_create_order_detail(db_session, mocker):
    mock_create_order_detail = mocker.patch.object(controller, 'create_order_detail', return_value=model.OrderDetail(id=1, order_id=1, dish_id=1, quantity=2))
    order_detail_request = {
        "order_id": 1,
        "dish_id": 1,
        "quantity": 2
    }
    response = client.post("/orders/1/details/", json=order_detail_request)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "order_id": 1, "dish_id": 1, "quantity": 2}

def test_update_order_detail(db_session, mocker):
    mock_update_order_detail = mocker.patch.object(controller, 'update_order_detail', return_value=model.OrderDetail(id=1, order_id=1, dish_id=1, quantity=2))
    order_detail_update_request = {
        "order_id": 1,
        "dish_id": 1,
        "quantity": 2
    }
    response = client.put("/orders/1/details/1", json=order_detail_update_request)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "order_id": 1, "dish_id": 1, "quantity": 2}

def test_delete_order_detail(db_session, mocker):
    mock_delete_order_detail = mocker.patch.object(controller, 'delete_order_detail', return_value=True)
    response = client.delete("/orders/1/details/1")
    assert response.status_code == 200
    assert response.json() == {"detail": "Order detail deleted successfully"}

