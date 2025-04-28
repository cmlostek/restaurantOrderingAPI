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


def test_read_all_users(db_session, mocker):
    mock_get_all_users = mocker.patch.object(controller, 'read_all_users', return_value=[model.User(id=1, name="Test User")])

    response = client.get("/users/")

    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Test User"}]

def test_read_user_by_id(db_session, mocker):
    mock_get_user_by_id = mocker.patch.object(controller, 'read_user_by_id', return_value=model.User(id=1, name="Test User"))



    response = client.get("/users/1")

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Test User"}

def test_create_new_user(db_session, mocker):
    mock_create_user = mocker.patch.object(controller, 'create_user', return_value=model.User(id=1, name="Test User"))

    user_request = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    }

    response = client.post("/users/", json=user_request)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Test User"}

    # mock_create_user.assert_called_once_with(db_session, user_request)

def test_update_existing_user(db_session, mocker):
    mock_update_user = mocker.patch.object(controller, 'update_user', return_value=model.User(id=1, name="Updated User"))

    user_request = {
        "id": 1,
        "name": "Updated Test User",
        "email": "test@example.com",
        "password": "password123"
    }

    response = client.put("/users/1", json=user_request)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Updated User"}

    # mock_update_user.assert_called_once_with(db_session, 1, user_request)

def test_delete_existing_user(db_session, mocker):
    mock_delete_user = mocker.patch.object(controller, 'delete_user', return_value=True)

    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json() == {"detail": "User deleted successfully"}

    # mock_delete_user.assert_called_once_with(db_session, 1)

def test_delete_non_existing_user(db_session, mocker):
    mock_delete_user = mocker.patch.object(controller, 'delete_user', return_value=False)

    response = client.delete("/users/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

    # mock_delete_user.assert_called_once_with(db_session, 1)

