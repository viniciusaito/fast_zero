from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_root_should_return_root_and_ola_bb():
    client = TestClient(app)  # Arrange

    response = client.get('/')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olá bb!'}  # Assert
