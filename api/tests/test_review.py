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


def test_get_all_reviews(db_session, mocker):
    mock_get_all_reviews = mocker.patch.object(controller, 'get_all_reviews', return_value=[model.Review(id=1, order_id=1, rating=5, comment="Great service!")])
    response = client.get("/orders/1/reviews/")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "order_id": 1, "rating": 5, "comment": "Great service!"}]

def test_get_review(db_session, mocker):
    mock_get_review = mocker.patch.object(controller, 'get_review', return_value=model.Review(id=1, order_id=1, rating=5, comment="Great service!"))
    response = client.get("/orders/1/reviews/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "order_id": 1, "rating": 5, "comment": "Great service!"}


def test_create_review(db_session, mocker):
    mock_create_review = mocker.patch.object(controller, 'create_review', return_value=model.Review(id=1, order_id=1, rating=5, comment="Great service!"))
    review_request = {
        "order_id": 1,
        "rating": 5,
        "comment": "Great service!"
    }
    response = client.post("/orders/1/reviews/", json=review_request)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "order_id": 1, "rating": 5, "comment": "Great service!"}

def test_update_review(db_session, mocker):
    mock_update_review = mocker.patch.object(controller, 'update_review', return_value=model.Review(id=1, order_id=1, rating=5, comment="Great service!"))
    review_update_request = {
        "review_id": 1,
        "order_id": 1,
        "rating": 5,
        "comment": "Great service!"
    }
    response = client.put("/orders/1/reviews/1", json=review_update_request)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "order_id": 1, "rating": 5, "comment": "Great service!"}

def test_delete_review(db_session, mocker):
    mock_delete_review = mocker.patch.object(controller, 'delete_review', return_value=True)
    response = client.delete("/orders/1/reviews/1")
    assert response.status_code == 200
    assert response.json() == {"detail": "Review deleted successfully"}

