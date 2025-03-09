from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from app.middlewares.logging_middleware import LoggingMiddleware
from app.utils.genreral_functions import create_storage_dirs
from app.api.routes import user

app = FastAPI()

# Call function at startup
create_storage_dirs()

app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)

