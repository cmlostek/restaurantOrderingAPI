from fastapi.testclient import TestClient
from ..controllers import orders as controller
from ..main import app
import pytest
from ..models import orders as model
from ..models.promotion import Promotion

# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_read_all_promotions(db_session, mocker):
    mock_get_all_promotions = mocker.patch.object(controller, 'read_all_promotions', return_value=[Promotion(id=1, name="Test Promotion")])

    response = client.get("/promotions/")

    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Test Promotion"}]

def test_read_promotion_by_id(db_session, mocker):
    mock_get_promotion_by_id = mocker.patch.object(controller, 'read_promotion', return_value=Promotion(id=1, name="Test Promotion"))

    response = client.get("/promotions/1")

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Test Promotion"}

def test_create_new_promotion(db_session, mocker):
    mock_create_promotion = mocker.patch.object(controller, 'create_new_promotion', return_value=Promotion(id=1, name="Test Promotion"))

    promotion_request = {
        "name": "Test Promotion",
        "description": "This is a test promotion",
        "discount_percentage": 10
    }

    response = client.post("/promotions/", json=promotion_request)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Test Promotion"}

def test_update_existing_promotion(db_session, mocker):
    mock_update_promotion = mocker.patch.object(controller, 'update_promotion', return_value=Promotion(id=1, name="Updated Promotion"))

    promotion_request = {
        "promotion_id": 1,
        "name": "Updated Test Promotion",
        "description": "This is an updated test promotion",
        "discount_percentage": 15
    }

    response = client.put("/promotions/1", json=promotion_request)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Updated Promotion"}

def test_delete_promotion(db_session, mocker):
    mock_delete_promotion = mocker.patch.object(controller, 'delete_promotion', return_value=True)

    response = client.delete("/promotions/1")
    assert response.status_code == 200
    assert response.json() == {"detail": "Promotion deleted successfully"}

def test_read_promotion_by_id_not_found(db_session, mocker):
    mock_get_promotion_by_id = mocker.patch.object(controller, 'read_promotion', return_value=None)

    response = client.get("/promotions/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Promotion not found"}

