from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username='xispeteo',
        email='xispeteo@xpto@to',
        password='securepassword',
    )

    session.add(user)
    session.commit()

    # session.refresh(user)
    session.scalar(select(User).where(User.email == 'xispeteo@xpto@to'))

    assert user.username == 'xispeteo'
    assert user.email == 'xispeteo@xpto@to'
    assert user.password == 'securepassword'
