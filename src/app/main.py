from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.app.db import init_db
from src.app.exception.globals import register_exception_handlers
from src.app.controller import (
    category_document_router,
    category_document_tags_metadata,
    role_router,
    role_tags_metadata,
    department_router,
    department_tags_metadata,
    documentary_topic_router,
    documentary_topic_tags_metadata,
    settlement_router,
    settlement_tags_metadata,
    submitter_router,
    submitter_tags_metadata,
    position_router,
    position_tags_metadata,
    employee_router,
    employee_tags_metadata,
    hamlet_router,
    hamlet_tags_metadata,
    area_router,
    area_connection_tags_metadata,
    user_router,
    user_tags_metadata,
)

API_PREFIX = "/api/v1"

tags_metadata = [
    category_document_tags_metadata,
    role_tags_metadata,
    department_tags_metadata,
    documentary_topic_tags_metadata,
    settlement_tags_metadata,
    submitter_tags_metadata,
    position_tags_metadata,
    employee_tags_metadata,
    hamlet_tags_metadata,
    area_connection_tags_metadata,
    user_tags_metadata,
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI application.
    Initializes the database and registers exception handlers.
    """
    await init_db()
    await register_exception_handlers(app)
    yield


app = FastAPI(
    title="File Track API",
    description="API for File Track",
    version="0.1.0",
    openapi_tags=tags_metadata,
    debug=True,
    lifespan=lifespan,
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Local server",
        },
    ],
    terms_of_service="https://opensource.org/licenses/MIT",
)

app.include_router(category_document_router, prefix=API_PREFIX)
app.include_router(role_router, prefix=API_PREFIX)
app.include_router(department_router, prefix=API_PREFIX)
app.include_router(documentary_topic_router, prefix=API_PREFIX)
app.include_router(settlement_router, prefix=API_PREFIX)
app.include_router(submitter_router, prefix=API_PREFIX)
app.include_router(position_router, prefix=API_PREFIX)
app.include_router(employee_router, prefix=API_PREFIX)
app.include_router(hamlet_router, prefix=API_PREFIX)
app.include_router(area_router, prefix=API_PREFIX)
app.include_router(user_router, prefix=API_PREFIX)
