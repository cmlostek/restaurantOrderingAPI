from fastapi.testclient import TestClient
from ..controllers import orders as controller
from ..main import app
import pytest
from ..models import orders as model
from ..models.payment import Payment

# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_read_all_payments(db_session, mocker):
    mock_get_all_payments = mocker.patch.object(controller, 'read_all_payments', return_value=[Payment(id=1, order_id=1, amount=100.0)])

    response = client.get("/payments/")

    assert response.status_code == 200
    assert response.json() == [{"id": 1, "order_id": 1, "amount": 100.0}]


def test_read_payment_by_id(db_session, mocker):
    mock_get_payment_by_id = mocker.patch.object(controller, 'read_payment', return_value=Payment(id=1, order_id=1, amount=100.0))

    response = client.get("/payments/1")

    assert response.status_code == 200
    assert response.json() == {"id": 1, "order_id": 1, "amount": 100.0}


def test_create_new_payment(db_session, mocker):
    mock_create_payment = mocker.patch.object(controller, 'create_new_payment', return_value=Payment(id=1, order_id=1, amount=100.0))

    payment_request = {
        "order_id": 1,
        "payment_method": "credit_card",
        "amount": 100.0
    }

    response = client.post("/payments/", json=payment_request)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "order_id": 1, "amount": 100.0}

def test_update_existing_payment(db_session, mocker):
    mock_update_payment = mocker.patch.object(controller, 'update_existing_payment', return_value=Payment(id=1, order_id=1, amount=100.0))

    payment_request = {
        "payment_id": 1,
        "order_id": 1,
        "payment_method": "cash",
        "amount": 100.0
    }

    response = client.put("/payments/1", json=payment_request)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "order_id": 1, "amount": 100.0}


def test_delete_payment(db_session, mocker):
    mock_delete_payment = mocker.patch.object(controller, 'delete_payment', return_value=True)

    response = client.delete("/payments/1")
    assert response.status_code == 200
    assert response.json() == {"detail": "Payment deleted successfully"}

