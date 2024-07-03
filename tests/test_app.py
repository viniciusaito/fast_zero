from http import HTTPStatus

from fast_zero.schemas import UserPublic


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
    success = client.post(
        '/users',
        json={
            'username': 'testusername',
            'email': 'test@test.com',
            'password': 'password',
        },
    )
    bad_request_username_exists = client.post(
        '/users',
        json={
            'username': 'testusername',
            'email': 'xpto@test.com',
            'password': 'password',
        },
    )
    bad_request_email_exists = client.post(
        '/users',
        json={
            'username': 'xpto',
            'email': 'test@test.com',
            'password': 'password',
        },
    )

    assert success.status_code == HTTPStatus.CREATED
    assert success.json() == {
        'username': 'testusername',
        'email': 'test@test.com',
        'id': 1,
    }
    assert bad_request_username_exists.status_code == HTTPStatus.BAD_REQUEST
    assert bad_request_username_exists.json() == {
        'detail': 'Username already exists'
    }
    assert bad_request_email_exists.status_code == HTTPStatus.BAD_REQUEST
    assert bad_request_email_exists.json() == {
        'detail': 'Email already exists'
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    success = client.get('/user/1')
    not_found = client.get('/user/2')

    assert success.status_code == HTTPStatus.OK
    assert success.json() == user_schema

    assert not_found.status_code == HTTPStatus.NOT_FOUND
    assert not_found.json() == {'detail': 'User ID not found'}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()
    update_test_user = {
        'username': 'vini',
        'email': 'vini@vini.com',
        'password': 'vini',
        'id': user.id,
    }
    success = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=update_test_user,
    )

    assert success.status_code == HTTPStatus.OK
    assert success.json() == user_schema


def test_delete_user(client, user, token):
    success = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert success.status_code == HTTPStatus.OK
    assert success.json() == {'message': 'User deleted'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token
