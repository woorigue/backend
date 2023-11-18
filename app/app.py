from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.blueprints import register_router
from app.core.errorhanlder import register_exception_handler
from starlette.middleware.sessions import SessionMiddleware


def create_application() -> FastAPI:
    application = FastAPI(
        title="우리들만의 리그 API",
        docs_url="/swagger",
    )
    application.add_middleware(SessionMiddleware, secret_key="testscret")
    register_router(application)
    register_exception_handler(application)
    return application


app = create_application()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
