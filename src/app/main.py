from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from src.app.core.db import init_db
from src.app.core.middleware import setup_cors_middleware
from src.app.core.exception import register_exception_handlers
from src.app.domain.document.service.dependencies import get_current_user
from src.app.domain.document.controller import (
    document_category_router,
    document_category_tags_metadata,
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
    department_connection_router,
    department_connection_tags_metadata,
    user_router,
    user_tags_metadata,
    auth_router,
    auth_tags_metadata,
    document_router,
    document_tags_metadata,
)

API_PREFIX = "/api/v1"

tags_metadata = [
    document_category_tags_metadata,
    role_tags_metadata,
    department_tags_metadata,
    documentary_topic_tags_metadata,
    settlement_tags_metadata,
    submitter_tags_metadata,
    position_tags_metadata,
    employee_tags_metadata,
    hamlet_tags_metadata,
    department_connection_tags_metadata,
    user_tags_metadata,
    auth_tags_metadata,
    document_tags_metadata,
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
    description=(
        "File Track API is a comprehensive document management system designed to streamline "
        "the tracking, storage, and management of official documents. It provides robust features "
        "for document lifecycle management including:\n\n"
        "- Secure document upload, storage, and retrieval\n"
        "- Advanced search and filtering capabilities\n"
        "- User authentication and role-based access control\n"
        "- Document categorization and metadata management\n"
        "- Employee and department management\n"
        "- Geographic organizational structure with settlements and hamlets\n"
        "- Complete audit trail for document processing\n\n"
        "This RESTful API enables organizations to digitally transform their document handling workflows, "
        "ensuring efficient processing, improved accessibility, and regulatory compliance. "
        "All endpoints are secured with OAuth2 authentication and fine-grained permission scopes."
    ),
    version="0.1.0",
    openapi_tags=tags_metadata,
    debug=True,
    lifespan=lifespan,
    contact={
        "name": "Roberto Ruben Chavez Vargas",
        "email": "robertoch263@gmail.com",
        "url": "https://github.com/RobertoRuben",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Local server",
        },
        {
            "url": "http://192.168.1.35:8000",
            "description": "Production server",
        },
    ],
    terms_of_service="https://opensource.org/licenses/MIT",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": 1,
        "deepLinking": True,
        "displayRequestDuration": True,
        "filter": True,
        "showExtensions": True,
        "syntaxHighlight.theme": "monokai",
    },
)

setup_cors_middleware(app)

app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(
    document_category_router,
    prefix=API_PREFIX,
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    role_router, prefix=API_PREFIX, dependencies=[Depends(get_current_user)]
)
app.include_router(
    department_router, prefix=API_PREFIX, dependencies=[Depends(get_current_user)]
)
app.include_router(
    documentary_topic_router,
    prefix=API_PREFIX,
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    settlement_router, prefix=API_PREFIX, dependencies=[Depends(get_current_user)]
)
app.include_router(
    submitter_router, prefix=API_PREFIX, dependencies=[Depends(get_current_user)]
)
app.include_router(
    position_router, prefix=API_PREFIX, dependencies=[Depends(get_current_user)]
)
app.include_router(
    employee_router, prefix=API_PREFIX, dependencies=[Depends(get_current_user)]
)
app.include_router(
    hamlet_router, prefix=API_PREFIX, dependencies=[Depends(get_current_user)]
)
app.include_router(
    department_connection_router,
    prefix=API_PREFIX,
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    user_router, prefix=API_PREFIX, dependencies=[Depends(get_current_user)]
)
app.include_router(
    document_router, prefix=API_PREFIX, dependencies=[Depends(get_current_user)]
)
