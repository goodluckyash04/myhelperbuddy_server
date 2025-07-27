from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from app.api.routes import ipo, user
from app.middlewares.logging_middleware import LoggingMiddleware
from app.utils.genreral_functions import create_storage_dirs

app = FastAPI()

# Call function at startup
create_storage_dirs()

app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/v1")
app.include_router(ipo.router, prefix="/v1")


@app.get("/")
async def read_root():
    return {"message": "Hello Welcome to myHelperBuddy!"}


def handler(req, context):
    return app(req, context)
