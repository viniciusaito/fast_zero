from http import HTTPStatus

from fast_zero.schemas import UserPublic


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
    success = client.get('users/1')
    not_found = client.get('/users/2')

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


def test_update_user_not_enough_permission(client, user, token):
    update_test_user = {
        'username': 'vini',
        'email': 'vini@vini.com',
        'password': 'vini',
        'id': user.id,
    }

    not_enough_permission = client.put(
        f'/users/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
        json=update_test_user,
    )

    assert not_enough_permission.status_code == HTTPStatus.FORBIDDEN
    assert not_enough_permission.json() == {'detail': 'Not enough permission'}


def test_delete_user(client, user, token):
    success = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert success.status_code == HTTPStatus.OK
    assert success.json() == {'message': 'User deleted'}


def test_delete_user_not_enough_permission(client, user, token):
    not_enough_permission = client.delete(
        f'/users/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert not_enough_permission.status_code == HTTPStatus.FORBIDDEN
    assert not_enough_permission.json() == {'detail': 'Not enough permission'}
