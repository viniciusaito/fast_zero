from http import HTTPStatus

from fastapi import testclient

from fast_zero.app import app


def test_read_root_deve_retornar_ok_e_ola_bb():
    client = testclient(app)  # Arrange (organização)

    response = client.get('/')  # Act (ação)

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json == {'message': 'Olá bb!'}
