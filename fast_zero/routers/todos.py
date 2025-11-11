from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import Todo, User
from fast_zero.schemas import (
    Message,
    TodoList,
    TodoPublic,
    TodoSchema,
    TodoState,
    TodoUpdate,
)
from fast_zero.security import get_current_user

router = APIRouter(prefix='/todos', tags=['todos'])

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=TodoPublic)
def create_todo(
    todo: TodoSchema,
    session: Session,
    user: CurrentUser,
):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.get('/', response_model=TodoList)
def list_todos(  # noqa
    session: Session,
    user: CurrentUser,
    title: str | None = None,
    description: str | None = None,
    state: TodoState | None = None,
    offset: int | None = None,
    limit: int | None = None,
):
    """
    Retrieve a list of TODOs for the current user with optional
    search and filtering.

    - Filter by title or description keywords (case-insensitive).
    - Filter by completion state.
    - Supports pagination via offset and limit.

    Args:
        session (Session): SQLAlchemy session dependency.
        user (User): Authenticated user dependency.
        title (str | None): Optional title keyword to search.
        description (str | None): Optional description keyword to search.
        state (TodoState | None): Optional state filter.
        offset (int | None): Optional pagination offset.
        limit (int | None): Optional pagination limit.

    Returns:
        dict: A dictionary containing the filtered list of TODOs.
    """
    query = select(Todo).where(Todo.user_id == user.id)

    if title:
        query = query.filter(Todo.title.ilike(f'%{title}%'))
    if description:
        query = query.filter(Todo.description.ilike(f'%{description}%'))
    if state:
        query = query.filter(Todo.state == state)

    if offset is not None:
        query = query.offset(offset)
    if limit is not None:
        query = query.limit(limit)

    todos = session.scalars(query).all()

    return {'todos': todos}


@router.delete('/{todo_id}', response_model=Message)
def delete_todo(todo_id: int, session: Session, user: CurrentUser):
    todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )
    return {'message': 'Task has been deleted successfully.'}


@router.patch('/{todo_id}', response_model=TodoPublic)
def patch_todo(
    todo_id: int, session: Session, user: CurrentUser, todo: TodoUpdate
):
    db_todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not db_todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo
