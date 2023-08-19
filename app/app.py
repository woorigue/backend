from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.blueprints import register_router


def create_application() -> FastAPI:
    application = FastAPI(
        title="우리들만의 리그 API",
        docs_url="/swagger",
    )
    register_router(application)
    return application


app = create_application()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
