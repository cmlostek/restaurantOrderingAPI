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


def test_create_order(db_session):
    # Create a sample order
    order_data = {
        "customer_name": "John Doe",
        "description": "Test order"

    }

    order_object = model.Order(**order_data)

    # Call the create function
    created_order = controller.create_guest_order(db_session, order_data)

    # Assertions
    assert created_order is not None
    assert created_order.customer_name == "John Doe"
    assert created_order.description == "Test order"

def test_create_guest_order(db_session):
    # Sample request payload
    order_data = {
        "total_price": 100.0,
        "dish_id": 1,
        "items": [
            {"product_id": 1, "quantity": 2},
            {"product_id": 2, "quantity": 1}
        ]
    }


    db_session.add = lambda x: None
    db_session.commit = lambda: None
    db_session.refresh = lambda x: None

    # post request
    response = client.post("/orders/guest", json=order_data)

    # tests
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["total_price"] == 100.0
    assert len(response_data["items"]) == 2
    assert response_data["items"][0]["product_id"] == 1
    assert response_data["items"][0]["quantity"] == 2