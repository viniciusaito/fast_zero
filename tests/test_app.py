from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_root_should_return_root_and_ola_bb():
    client = TestClient(app)  # Arrange

    response = client.get('/')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olá bb!'}  # Assert


def test_olamundo_should_return_html_with_ola_mundo():
    client = TestClient(app)

    response = client.get('/olamundo')

    assert response.status_code == HTTPStatus.OK
    assert response.text == """
    <html>
      <head>
        <title> Nosso olá mundo!</title>
      </head>
      <body>
        <h1> Olá Mundo </h1>
      </body>
    </html>
    """
