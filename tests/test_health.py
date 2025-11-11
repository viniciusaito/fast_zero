from unittest.mock import MagicMock
from sqlalchemy.exc import SQLAlchemyError
from http import HTTPStatus

def test_health_check_ok(client):
    response = client.get("/health")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "app_status": "ok",
        "database_status": "ok",
        "timestamp": response.json()["timestamp"],
    }

def test_health_check_error(client, session):
    session.execute = MagicMock(side_effect=SQLAlchemyError)
    response = client.get("/health")

    assert response.status_code == HTTPStatus.SERVICE_UNAVAILABLE
    assert response.json() == {
        "app_status": "error",
        "database_status": "error",
        "timestamp": response.json()["timestamp"],
    }
