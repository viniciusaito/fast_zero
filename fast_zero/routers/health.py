"""Health check endpoint for application and database readiness.

This module exposes a health check endpoint that verifies:
- Application availability
- Database connectivity (via a lightweight `SELECT 1`)

It returns a JSON payload containing:
- app_status: "ok" | "error"
- database_status: "ok" | "error"
- timestamp: ISO 8601 (UTC) timestamp

HTTP 200 is returned when both the app and database are healthy.
HTTP 503 (Service Unavailable) is returned when the database check fails.
"""

from __future__ import annotations

from datetime import datetime, timezone
from http import HTTPStatus
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Response
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.schemas import HealthCheck

router = APIRouter(prefix='/health', tags=['health'])

# Dependency alias, following the pattern from todos.py
SessionDep = Annotated[Session, Depends(get_session)]


@router.get(
    '/',
    response_model=HealthCheck,
    summary='Health check',
    description=(
        """
        Returns application and database health
        status with a timestamp.
        Responds with 200 when healthy and 503
        when the database is unavailable.
    """
    ),
)
def health_check(session: SessionDep, response: Response) -> HealthCheck:
    """Health check endpoint.

    Performs a lightweight database connectivity verification using `SELECT 1`.
    Sets HTTP status to 503 if the database is not reachable.

    Args:
        session: SQLAlchemy session provided by dependency injection.
        response: FastAPI response object
        (used to set the appropriate status code).

    Returns:
        HealthCheck: Health status payload containing app_status,
        database_status, and timestamp.
    """
    database_status: Literal['ok', 'error'] = 'ok'

    try:
        # Lightweight DB connectivity check
        session.execute(text('SELECT 1'))
    except SQLAlchemyError:
        database_status = 'error'

    # Set HTTP status code based on DB status
    response.status_code = (
        HTTPStatus.OK
        if database_status == 'ok'
        else HTTPStatus.SERVICE_UNAVAILABLE
    )

    return HealthCheck(
        app_status='ok' if database_status == 'ok' else 'error',
        database_status=database_status,
        timestamp=datetime.now(timezone.utc),
    )
