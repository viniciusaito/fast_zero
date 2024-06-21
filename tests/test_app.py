from http import HTTPStatus


def test_root_should_return_root_and_ola_bb(client):
    response = client.get('/')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olá bb!'}  # Assert


def test_olamundo_should_return_html_with_ola_mundo(client):
    response = client.get('/olamundo')

    assert response.status_code == HTTPStatus.OK
    assert (
        response.text
        == """
    <html>
      <head>
        <title> Nosso olá mundo!</title>
      </head>
      <body>
        <h1> Olá Mundo </h1>
      </body>
    </html>
    """
    )


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'testusername',
            'password': 'password',
            'email': 'test@test.com',
        },
    )

    # Validar status code
    assert response.status_code == HTTPStatus.CREATED
    # Validar UserPublic
    assert response.json() == {
        'username': 'testusername',
        'email': 'test@test.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {'username': 'testusername', 'email': 'test@test.com', 'id': 1}
        ]
    }


def test_update_user(client):
    test_user = {
        'username': 'testusername',
        'email': 'test@test.com',
        'password': 'password',
    }
    response = client.put(
        '/users/1',
        json=test_user,
    )
    response_404_user_above_max = client.put(
        '/users/2',
        json=test_user,
    )
    response_404_user_below_min = client.put(
        '/users/0',
        json=test_user,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'testusername',
        'email': 'test@test.com',
        'id': 1,
    }
    assert response_404_user_above_max.status_code == HTTPStatus.NOT_FOUND
    assert response_404_user_above_max.json() == {'detail': 'User not found'}
    assert response_404_user_below_min.status_code == HTTPStatus.NOT_FOUND
    assert response_404_user_below_min.json() == {'detail': 'User not found'}


def test_delete_user(client):
    response = client.delete('/users/1')
    response_404_user_above_max = client.delete('/users/2')
    response_404_user_below_min = client.delete('/users/0')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}
    assert response_404_user_above_max.status_code == HTTPStatus.NOT_FOUND
    assert response_404_user_above_max.json() == {'detail': 'User not found'}
    assert response_404_user_below_min.status_code == HTTPStatus.NOT_FOUND
    assert response_404_user_below_min.json() == {'detail': 'User not found'}
