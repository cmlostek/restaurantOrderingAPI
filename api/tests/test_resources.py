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


def test_create_new_resource(db_session, mocker):
    # mocking function
    mock_create_resource = mocker.patch.object(controller, 'create_resource', return_value=model.Resource(id=1, name="Test Resource"))

    # sample resource request
    resource_request = {
        "resource_id": 1,
        "resource_name": "Test Resource",
        "resource_type": "Type A",
        "quantity_available": 10
    }

    # make a post-request to create a resource
    response = client.post("/resources/", json=resource_request)

    # asserting the response for the resource
    assert response.status_code == 200
    assert response.json() == {
        "resource_id": 1,
        "resource_name": "Test Resource",
        "resource_type": "Type A",
        "quantity_available": 10
    }


def test_read_all_resources(db_session, mocker):
    mock_get_all_resources = mocker.patch.object(controller, 'get_all_resources', return_value=[model.Resource(id=1, name="Test Resource")])

    response = client.get("/resources/")

    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Test Resource"}]

def test_update_existing_resource(db_session, mocker):
    mock_update_resource = mocker.patch.object(controller, 'update_resource', return_value=model.Resource(id=1, name="Updated Resource"))

    resource_update_request = {
        "resource_id": 1,
        "resource_name": "Updated Resource",
        "resource_type": "Type B",
        "quantity_available": 5
    }

    response = client.put("/resources/1", json=resource_update_request)
    assert response.status_code == 200
    assert response.json() == {
        "resource_id": 1,
        "resource_name": "Updated Resource",
        "resource_type": "Type B",
        "quantity_available": 5
    }

def test_delete_existing_resource(db_session, mocker):
    mock_delete_resource = mocker.patch.object(controller, 'delete_resource', return_value=True)

    response = client.delete("/resources/1")
    assert response.status_code == 200
    assert response.json() == {"detail": "Resource deleted successfully"}

def test_read_resource_by_id(db_session, mocker):
    mock_read_resource_by_id = mocker.patch.object(controller, 'read_resource_by_id', return_value=model.Resource(id=1, name="Test Resource"))

    response = client.get("/resources/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Test Resource"}


